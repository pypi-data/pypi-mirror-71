import time
from datetime import datetime

from babel.numbers import format_number
from flask import (abort, current_app, make_response, redirect, render_template, request,
                   send_from_directory, url_for)
from flask_babelex import get_locale, gettext, ngettext

from . import babel_domain, blueprint
from .attachments import get_attachments_dir
from .breadbox import build_breadbox
from .criteria import Criteria
from .forms import SearchForm
from .pager import build_pager
from .query import build_creators_display, build_item_facet_results, run_query, run_query_unique
from .sorter import build_sorter


def get_search_return_fields(criteria):
    if criteria.page_len != 1:  # Note: page_len can be None (for all results).
        return_fields = current_app.config['KERKO_RESULTS_FIELDS']
        if current_app.config['KERKO_RESULTS_ABSTRACT'] and 'data' not in return_fields:
            return_fields.append('data')
        for badge in current_app.config['KERKO_COMPOSER'].badges.values():
            if badge.field.key not in return_fields:
                return_fields.append(badge.field.key)
        return return_fields
    return None  # All fields.


@blueprint.route('/', methods=['GET', 'POST'])
def search():
    """View the results of a search."""
    start_time = time.process_time()

    if current_app.config['KERKO_USE_TRANSLATIONS']:
        babel_domain.as_default()

    criteria = Criteria(request)
    form = SearchForm(csrf_enabled=False)
    if form.validate_on_submit():
        url = criteria.build_add_keywords_url(
            scope=form.scope.data,
            value=form.keywords.data)
        return redirect(url, 302)

    search_results, facet_results, total_count, page_count, last_sync = run_query(
        criteria, get_search_return_fields(criteria)
    )

    breadbox = build_breadbox(criteria, facet_results)
    context = {
        'facet_results': facet_results,
        'breadbox': breadbox,
        'active_facets': breadbox['filters'].keys() if 'filters' in breadbox else [],
        'pager': build_pager(criteria, page_count, criteria.page_len),
        'sorter': build_sorter(criteria),
        'total_count': total_count,
        'total_count_formatted': format_number(total_count, locale=get_locale()),
        'page_count': page_count,
        'page_count_formatted': format_number(page_count, locale=get_locale()),
        'page_len': criteria.page_len,
        'is_searching': criteria.has_keyword_search() or criteria.has_filter_search(),
        'locale': get_locale(),
        'last_sync': datetime.fromtimestamp(last_sync).strftime('%Y-%m-%d %H:%M') if last_sync else '',
    }

    if criteria.page_len == 1 and total_count != 0:
        list_page_num = int((criteria.page_num - 1) / current_app.config['KERKO_PAGE_LEN'] + 1)
        build_creators_display(search_results[0])
        build_item_facet_results(search_results[0])
        return render_template(
            current_app.config['KERKO_TEMPLATE_SEARCH_ITEM'],
            title=search_results[0].get('data', {}).get('title', ''),
            item=search_results[0],
            item_url=url_for(
                '.item_view', item_id=search_results[0]['id'], _external=True
            ) if search_results[0] else '',
            back_url=criteria.build_url(page_num=list_page_num),
            time=time.process_time() - start_time,
            **context
        )

    if total_count > 0:
        for i, result in enumerate(search_results):
            result['url'] = criteria.build_url(
                page_num=(criteria.page_num - 1) * (criteria.page_len or 0) + i + 1,
                page_len=1
            )
        if context['is_searching']:
            context['title'] = ngettext('Result', 'Results', total_count)
        else:
            context['title'] = gettext('Full bibliography')
    else:
        context['title'] = gettext('Your search did not match any resources')
    return render_template(
        current_app.config['KERKO_TEMPLATE_SEARCH'],
        form=form,
        search_results=search_results,
        print_url=criteria.build_url(page_len='all', print_preview=True),
        print_preview=criteria.print_preview,
        download_urls={
            key: criteria.build_download_url(key)
            for key in current_app.config['KERKO_COMPOSER'].citation_formats.keys()
        },
        time=time.process_time() - start_time,
        **context
    )


@blueprint.route('/<string:item_id>')
def item_view(item_id):
    """View a full bibliographic record."""
    start_time = time.process_time()

    if current_app.config['KERKO_USE_TRANSLATIONS']:
        babel_domain.as_default()

    item = run_query_unique('id', item_id)
    if not item:
        abort(404)

    build_creators_display(item)
    build_item_facet_results(item)
    return render_template(
        current_app.config['KERKO_TEMPLATE_ITEM'],
        item=item,
        title=item.get('data', {}).get('title', ''),
        item_url=url_for('.item_view', item_id=item_id, _external=True) if item else '',
        time=time.process_time() - start_time,
        locale=get_locale(),
    )


@blueprint.route('/<string:item_id>/download/<string:attachment_id>/')
@blueprint.route('/<string:item_id>/download/<string:attachment_id>/<string:attachment_filename>')
def item_attachment_download(item_id, attachment_id, attachment_filename=None):
    """
    Download an item attachment.

    If the URL does not specify the attachment's filename or provides the wrong
    filename, a redirect is performed to a corrected URL so that the client gets
    a proper filename.
    """
    if current_app.config['KERKO_USE_TRANSLATIONS']:
        babel_domain.as_default()

    item = run_query_unique('id', item_id)
    if not item:
        abort(404)

    matching_attachments = list(
        filter(lambda a: a.get('id') == attachment_id, item.get('attachments', []))
    )
    if not matching_attachments or len(matching_attachments) > 1:
        abort(404)
    attachment = matching_attachments[0]

    filepath = get_attachments_dir() / attachment_id
    if not filepath.exists():
        abort(404)

    if attachment_filename != attachment['filename']:
        return redirect(
            url_for(
                'kerko.item_attachment_download',
                item_id=item_id,
                attachment_id=attachment_id,
                attachment_filename=attachment['filename'],
            ), 301
        )

    return send_from_directory(
        get_attachments_dir(),
        attachment_id,
        mimetype=attachment['mimetype'],
    )


@blueprint.route('/<string:item_id>/<string:citation_format_key>')
def item_citation_download(item_id, citation_format_key):
    """Download a citation."""
    if current_app.config['KERKO_USE_TRANSLATIONS']:
        babel_domain.as_default()

    item = run_query_unique('id', item_id)
    if not item:
        abort(404)

    citation_format = current_app.config['KERKO_COMPOSER'].citation_formats.get(citation_format_key)
    if not citation_format:
        abort(404)

    content = item.get(citation_format.field.key)
    if not content:
        abort(404)

    response = make_response(content)
    response.headers['Content-Disposition'] = \
        f'attachment; filename={item_id}.{citation_format.extension}'
    response.headers['Content-Type'] = \
        f'{citation_format.mime_type}; charset=utf-8'
    return response


@blueprint.route('/download/<string:citation_format_key>/')
def search_citation_download(citation_format_key):
    """Download all citations resulting from a search."""
    citation_format = current_app.config['KERKO_COMPOSER'].citation_formats.get(citation_format_key)
    if not citation_format:
        abort(404)

    criteria = Criteria(request)
    criteria.page_len = None

    search_results, _, total_count, _, _ = run_query(  # TODO: Avoid building facet results.
        criteria, return_fields=[citation_format.field.key]
    )

    if total_count == 0:
        abort(404)

    citations = [result.get(citation_format.field.key, '') for result in search_results]
    response = make_response(
        citation_format.group_format.format(
            citation_format.group_item_delimiter.join(citations)
        )
    )
    response.headers['Content-Disposition'] = \
        f'attachment; filename=bibliography.{citation_format.extension}'  # TODO: Make filename configurable.
    response.headers['Content-Type'] = \
        f'{citation_format.mime_type}; charset=utf-8'
    return response

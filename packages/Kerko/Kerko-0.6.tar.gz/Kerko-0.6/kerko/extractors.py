"""
Functions for extracting data from Zotero items.
"""

from abc import ABC, abstractmethod
from collections import defaultdict
import re

from flask import current_app, Markup

from .text import id_normalize, sort_normalize


RECORD_SEPARATOR = '\x1e'


class ItemContext:
    """Contains data related to a Zotero item."""

    def __init__(self, item, children):
        """
        Initialize an item's data.

        :param dict item: An item, as returned by the Zotero API.

        :param list children: A list of dicts representing the item's children.
        """
        self.item_key = item.get('key', '')  # For convenient access.
        self.item = item
        self.children = children
        self.data = item.get('data', {})  # For convenient access.


class LibraryContext:
    """Contains data related to a Zotero library."""

    def __init__(self, collections, item_types, item_fields, creator_types):
        self.collections = collections
        self.item_types = item_types
        self.item_fields = item_fields
        self.creator_types = creator_types

    def get_creator_types(self, item_data):
        return self.creator_types.get(item_data.get('itemType', ''), [])


def _parse_zotero_date(text):
    """Parse a fuzzy date into a (year, month, day) tuple of numerical values."""
    year = month = day = 0
    matches = re.match(r'^([0-9]{4})(-([0-9]{2})(-([0-9]{2}))?)?', text)
    if matches:
        if matches.group(1):
            year = int(matches.group(1))
        if matches.group(3):
            month = int(matches.group(3))
        if matches.group(5):
            day = int(matches.group(5))
    return year, month, day


class Extractor(ABC):

    def __init__(self, format_='data'):
        """
        Initialize the extractor.

        :param str format_: Format required when performing the Zotero read.
        """
        self.format = format_

    @abstractmethod
    def extract(self, document, spec, item_context, library_context):
        """Extract a value from context and store it in document using spec."""

    def warning(self, message, item_context):
        current_app.logger.warning(
            f"{self.__class__.__name__}: {message} ({item_context.item_key})"
        )


class KeyExtractor(Extractor):  # pylint: disable=abstract-method

    def __init__(self, key, **kwargs):
        """
        Initialize the extractor.

        :param str key: Key of the element to extract from the Zotero item.
        """
        super().__init__(**kwargs)
        self.key = key


class ItemExtractor(KeyExtractor):
    """Extract a value from an item."""

    def extract(self, document, spec, item_context, library_context):
        if self.key in item_context.item:
            document[spec.key] = spec.encode(item_context.item[self.key])


class ItemDataExtractor(KeyExtractor):
    """Extract a value from item data."""

    def extract(self, document, spec, item_context, library_context):
        if self.key in item_context.data:
            document[spec.key] = spec.encode(item_context.data[self.key])


class RawDataExtractor(Extractor):

    def extract(self, document, spec, item_context, library_context):
        document[spec.key] = spec.encode(item_context.data)


class ItemTypeLabelExtractor(Extractor):
    """Extract the label of the item's type."""

    def extract(self, document, spec, item_context, library_context):
        item_type = item_context.data.get('itemType')
        if item_type and item_type in library_context.item_types:
            document[spec.key] = spec.encode(library_context.item_types[item_type])
        else:
            self.warning("Missing itemType", item_context)


class ItemFieldsExtractor(Extractor):
    """Extract field metadata, serialized as a JSON string."""

    def extract(self, document, spec, item_context, library_context):
        item_type = item_context.data.get('itemType')
        if item_type and item_type in library_context.item_fields:
            fields = library_context.item_fields[item_type]
            # Retain metadata for fields that are actually present in the item.
            item_fields = [f for f in fields if f.get('field') in item_context.data]
            if item_fields:
                document[spec.key] = spec.encode(item_fields)
            else:
                self.warning("Missing item type fields", item_context)
        else:
            self.warning("Missing itemType", item_context)


class CreatorTypesExtractor(Extractor):
    """Extract creator types metadata, serialized as a JSON string."""

    def extract(self, document, spec, item_context, library_context):
        item_type = item_context.data.get('itemType')
        if item_type and item_type in library_context.creator_types:
            library_creator_types = library_context.creator_types[item_type]
            # Retain metadata for creator types that are actually present in the item.
            item_creator_types = []
            for library_creator_type in library_creator_types:
                for item_creator in item_context.data.get('creators', []):
                    creator_type = item_creator.get('creatorType')
                    if creator_type and creator_type == library_creator_type.get('creatorType'):
                        item_creator_types.append(library_creator_type)
                        break
            if item_creator_types:
                document[spec.key] = spec.encode(item_creator_types)
            elif item_context.data.get('creators', False):
                self.warning("Missing creator types", item_context)
        else:
            self.warning("Missing itemType", item_context)


class CreatorsExtractor(Extractor):
    """Flatten and extract creator data."""

    def extract(self, document, spec, item_context, library_context):
        creators = []
        if 'creators' in item_context.data:
            for creator in item_context.data['creators']:
                n = creator.get('name', '').strip()
                if n:
                    creators.append(n)
                firstname = creator.get('firstName', '').strip()
                lastname = creator.get('lastName', '').strip()
                if firstname and lastname:
                    # Combine firstname and lastname in different orders to help
                    # phrase searches.
                    creators.append(' '.join([firstname, lastname]))
                    creators.append(', '.join([lastname, firstname]))
                elif firstname:
                    creators.append(firstname)
                elif lastname:
                    creators.append(lastname)
        if creators:
            document[spec.key] = spec.encode(RECORD_SEPARATOR.join(creators))


class CollectionNamesExtractor(Extractor):
    """Extract item collections for text search."""

    def extract(self, document, spec, item_context, library_context):
        names = set()
        if 'collections' in item_context.data:
            for k in item_context.data['collections']:
                if k in library_context.collections:
                    name = library_context.collections[k].get('data', {}).get('name', '').strip()
                    if name:
                        names.add(name)
        if names:
            document[spec.key] = spec.encode(RECORD_SEPARATOR.join(names))


class BaseTagsExtractor(Extractor):

    def __init__(self, whitelist_re='', blacklist_re='', **kwargs):
        """
        Initialize the extractor.

        :param str whitelist_re: Any tag that does not matches this regular
            expression will be ignored by the extractor. If empty, all tags will
            be accepted unless `blacklist_re` is set and they match it.

        :param str blacklist_re: Any tag that matches this regular expression
            will be ignored by the extractor. If empty, all tags will be
            accepted unless `whitelist_re` is set and they do not match it.
        """
        super().__init__(**kwargs)
        self.whitelist = re.compile(whitelist_re) if whitelist_re else None
        self.blacklist = re.compile(blacklist_re) if blacklist_re else None

    def extract(self, document, spec, item_context, library_context):
        tags = set()
        if 'tags' in item_context.data:
            for tag_data in item_context.data['tags']:
                tag = tag_data.get('tag', '').strip()
                if tag and \
                        (not self.whitelist or self.whitelist.match(tag)) and \
                        (not self.blacklist or not self.blacklist.match(tag)):
                    tags.add(tag)
        if tags:
            self.to_document(document, spec, tags)

    @abstractmethod
    def to_document(self, document, spec, tags):
        """Assign the extracted value to the document."""


class TagsTextExtractor(BaseTagsExtractor):
    """Extract item tags for text search."""

    def to_document(self, document, spec, tags):
        document[spec.key] = spec.encode(RECORD_SEPARATOR.join(tags))


class BaseChildrenExtractor(Extractor):

    def __init__(self, item_type, whitelist_re='', blacklist_re='', **kwargs):
        """
        Initialize the extractor.

        :param str item_type: The type of child items to extract, either 'note'
            or 'attachment'.

        :param str whitelist_re: Any child which does not have a tag that
            matches this regular expression will be ignored by the extractor. If
            empty, all children will be accepted unless `blacklist_re` is set
            and causes some to be rejected.

        :param str blacklist_re: Any child that have a tag that matches this
            regular expression will be ignored by the extractor. If empty, all
            children will be accepted unless `whitelist_re` is set and causes
            some to be rejected.
        """
        super().__init__(**kwargs)
        self.item_type = item_type
        self.whitelist = re.compile(whitelist_re) if whitelist_re else None
        self.blacklist = re.compile(blacklist_re) if blacklist_re else None

    def extract(self, document, spec, item_context, library_context):
        accepted_children = []
        for child in item_context.children:
            if child.get('data', {}).get('itemType') == self.item_type:
                whitelisted = self.whitelist is None
                blacklisted = False
                if self.whitelist or self.blacklist:
                    for tag_data in child.get('data', {}).get('tags', []):
                        tag = tag_data.get('tag', '').strip()
                        if self.whitelist and self.whitelist.match(tag):
                            whitelisted = True
                        if self.blacklist and self.blacklist.match(tag):
                            blacklisted = True
                if whitelisted and not blacklisted:
                    accepted_children.append(child)
        if accepted_children:
            self.to_document(document, spec, accepted_children)

    @abstractmethod
    def to_document(self, document, spec, children):
        """Assign the extracted children to the document."""


class AttachmentsExtractor(BaseChildrenExtractor):
    """
    Extract attachments into a list of dicts for storage.

    This extractor only extracts a subset of attachment data provided by Zotero.
    """

    def __init__(self, mime_types=None, **kwargs):
        self.mime_types = mime_types
        super().__init__(item_type='attachment', **kwargs)

    def to_document(self, document, spec, children):
        document[spec.key] = spec.encode(
            [
                {
                    'id': a['key'],
                    'mimetype': a['data'].get('contentType', 'octet-stream'),
                    'filename': a['data'].get('filename', a['key']),
                    'md5': a['data'].get('md5', ''),
                    'mtime': a['data'].get('mtime', 0),
                } for a in children if a.get('data') and a.get('key') and (
                    not self.mime_types or a.get('data', {}).get(
                        'contentType', 'octet-stream'
                    ) in self.mime_types
                )
            ]
        )


class BaseNotesExtractor(BaseChildrenExtractor):  # pylint: disable=abstract-method

    def __init__(self, **kwargs):
        super().__init__(item_type='note', **kwargs)


class NotesTextExtractor(BaseNotesExtractor):
    """Extract notes for text search."""

    def to_document(self, document, spec, children):
        document[spec.key] = spec.encode(
            RECORD_SEPARATOR.join(
                [
                    Markup(child.get('data', {}).get('note', '')).striptags()
                    for child in children
                ]
            )
        )


class RawNotesExtractor(BaseNotesExtractor):
    """Extract raw notes for storage."""

    def to_document(self, document, spec, children):
        document[spec.key] = spec.encode(
            [child.get('data', {}).get('note', '') for child in children]
        )


def _expand_paths(path):
    """
    Extract the paths of each of the components of the specified path.

    If the given path is ['a', 'b', 'c'], the returned list of paths is:
    [['a'], ['a', 'b'], ['a', 'b', 'c']]
    """
    return [path[0:i + 1] for i in range(len(path))]


class CollectionFacetTreeExtractor(Extractor):
    """Index the Zotero item's collections needed for the specified facet."""

    def extract(self, document, spec, item_context, library_context):
        # Sets prevent duplication when multiple collections share common ancestors.
        encoded_ancestors = defaultdict(set)

        for collection_key in item_context.data.get('collections', []):
            if collection_key not in library_context.collections:
                continue  # Skip unknown collection.
            ancestors = library_context.collections.ancestors(collection_key)
            if len(ancestors) <= 1 or ancestors[0] != spec.collection_key:
                continue  # Skip collection, unrelated to this facet.

            ancestors = ancestors[1:]  # Facet values come from subcollections.
            for path in _expand_paths(ancestors):
                label = library_context.collections.get(
                    path[-1], {}
                ).get('data', {}).get('name', '').strip()
                encoded_ancestors[spec.key].add(spec.encode((path, label)))

        for key, ancestors in encoded_ancestors.items():
            document[key] = list(ancestors)


class InCollectionExtractor(Extractor):
    """Extract the boolean membership of an item into a collection."""

    def __init__(self, collection_key, true_only=True, **kwargs):
        super().__init__(**kwargs)
        self.collection_key = collection_key
        self.true_only = true_only

    def extract(self, document, spec, item_context, library_context):
        is_in = self.collection_key in item_context.data.get('collections', [])
        if not self.true_only:
            document[spec.key] = spec.encode(is_in)
        elif is_in:
            document[spec.key] = spec.encode(True)


class TagsFacetExtractor(BaseTagsExtractor):
    """Index the Zotero item's tags for faceting."""

    def to_document(self, document, spec, tags):
        document[spec.key] = [spec.encode(tag) for tag in tags]


class ItemTypeFacetExtractor(Extractor):
    """Index the Zotero item's type for faceting."""

    def extract(self, document, spec, item_context, library_context):
        item_type = item_context.data.get('itemType')
        if item_type:
            document[spec.key] = spec.encode(
                (item_type, library_context.item_types.get(item_type, item_type))
            )
        else:
            self.warning("Missing itemType", item_context)


class YearFacetExtractor(Extractor):
    """Index the Zotero item's publication date for faceting by year."""

    def extract(self, document, spec, item_context, library_context):
        parsed_date = item_context.item.get('meta', {}).get('parsedDate', '')
        if parsed_date:
            year, _month, _day = _parse_zotero_date(parsed_date)
            decade = int(int(year) / 10) * 10
            century = int(int(year) / 100) * 100
            encoded_paths = [
                spec.encode(path) for path in _expand_paths(
                    [str(century), str(decade), str(year)]
                )
            ]
            document[spec.key] = encoded_paths


class ItemDataLinkFacetExtractor(ItemDataExtractor):

    def extract(self, document, spec, item_context, library_context):
        document[spec.key] = spec.encode(item_context.data.get(self.key, '').strip() != '')


def _prepare_sort_text(text):
    """
    Normalize the given text for a sort field.

    Sort fields are bytearrays in the schema, so the text goes through
    str.encode().

    :param str text: The Unicode string to normalize.

    :return bytearray: The normalized text.
    """
    return sort_normalize(Markup(text).striptags()).encode()


class SortItemDataExtractor(ItemDataExtractor):

    def extract(self, document, spec, item_context, library_context):
        document[spec.key] = spec.encode(
            _prepare_sort_text(item_context.data.get(self.key, ''))
        )


class SortCreatorExtractor(Extractor):

    def extract(self, document, spec, item_context, library_context):
        creators = []

        def append_creator(creator):
            creator_parts = [
                _prepare_sort_text(creator.get('lastName', '')),
                _prepare_sort_text(creator.get('firstName', '')),
                _prepare_sort_text(creator.get('name', ''))]
            creators.append(b' zzz '.join([p for p in creator_parts if p]))

        # We treat creator types like an ordered list, where the first creator
        # type is for primary creators. Depending on the citation style, lesser
        # creator types may not appear in citations. Therefore, we try to sort
        # only by primary creators in order to avoid sorting with data that may
        # be invisible to the user. Only when an item has no primary creator do
        # we fallback to lesser creators.
        for creator_type in library_context.get_creator_types(item_context.data):
            for creator in item_context.data.get('creators', []):
                if creator.get('creatorType', '') == creator_type.get('creatorType'):
                    append_creator(creator)
            if creators:
                break  # No need to include lesser creator types.
        document[spec.key] = spec.encode(b' zzzzzz '.join(creators))


class SortDateExtractor(Extractor):

    def extract(self, document, spec, item_context, library_context):
        parsed_date = item_context.item.get('meta', {}).get('parsedDate', '')
        year, month, day = _parse_zotero_date(parsed_date)
        document[spec.key] = spec.encode(
            int('{:04d}{:02d}{:02d}'.format(year, month, day))
        )

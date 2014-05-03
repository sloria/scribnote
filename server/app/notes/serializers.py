# -*- coding: utf-8 -*-

from ..extensions import ma
from ..books.serializers import BookMarshal

class NoteMarshal(ma.Serializer):
    class Meta:
        dateformat = 'iso'
        additional = ('id', 'text', )
    created = ma.DateTime(attribute='date_created')
    book = ma.Nested(BookMarshal)
    _links = ma.Hyperlinks({
        'collection': ma.URL('notes.NoteList:get'),
    })

# Create factory functions which set strict mode as default
serialize_note = NoteMarshal.factory(strict=True)

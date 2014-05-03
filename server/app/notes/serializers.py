# -*- coding: utf-8 -*-
from flask.ext.marshmallow import Serializer, fields

from ..books.serializers import BookMarshal

class NoteMarshal(Serializer):
    class Meta:
        dateformat = 'iso'
        additional = ('id', 'text', )
    created = fields.DateTime(attribute='date_created')
    book = fields.Nested(BookMarshal)
    _links = fields.Hyperlinks({
        'collection': fields.URL('notes.NoteList:get'),
    })

# Create factory functions which set strict mode as default
serialize_note = NoteMarshal.factory(strict=True)

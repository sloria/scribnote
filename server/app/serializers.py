# -*- coding: utf-8 -*-
#
from flask.ext.marshmallow import Serializer, fields


# Serializers

class BaseBookMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    _links = fields.Hyperlinks({
        'self': fields.URL('books.BookDetail:get', id='<id>', _external=True),
        'collection': fields.URL('books.BookList:get', _external=True),
    })

    class Meta:
        additional = ('id', 'title', 'isbn')


class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')
    books = fields.Nested(BaseBookMarshal, many=True)

    # Implement HATEOAS
    _links = fields.Hyperlinks({
        'self': fields.AbsoluteURL('books.AuthorDetail:get', id='<id>'),
        'update': fields.AbsoluteURL('books.AuthorDetail:put', id='<id>'),
        'collection': fields.AbsoluteURL('books.AuthorList:get'),
    })

    class Meta:
        additional = ('id', 'first', 'last')

class BookMarshal(BaseBookMarshal):
    author = fields.Nested(AuthorMarshal, allow_null=True)




class NoteMarshal(Serializer):
    class Meta:
        additional = ('text', )
    created = fields.DateTime(attribute='date_created')
    book = fields.Nested(BookMarshal)
    _links = fields.Hyperlinks({
        'collection': fields.URL('notes.NoteList:get'),
    })

# Create factory methods which set strict mode as default
serialize_author = AuthorMarshal.factory(strict=True)
serialize_book = BookMarshal.factory(strict=True)
serialize_note = NoteMarshal.factory(strict=True)

# -*- coding: utf-8 -*-
#
from ..extensions import ma

class AuthorMarshal(ma.Serializer):
    """Defines the represention of an Author."""
    created = ma.DateTime(attribute='date_created')
    books = ma.Nested('BookMarshal', many=True, only=('id', 'title'))

    _links = ma.Hyperlinks({
        'self': ma.AbsoluteURL('books.AuthorDetail:get', id='<id>'),
        'update': ma.AbsoluteURL('books.AuthorDetail:put', id='<id>'),
        'collection': ma.AbsoluteURL('books.AuthorList:get'),
    })

    class Meta:
        dateformat = 'iso'
        additional = ('id', 'first', 'last')

class BookMarshal(ma.Serializer):
    """Defines the representation of a Book."""
    created = ma.DateTime(attribute='date_created')
    author = ma.Nested(AuthorMarshal, exclude=('books', ), allow_null=True)

    _links = ma.Hyperlinks({
        'self': ma.AbsoluteURL('books.BookDetail:get', id='<id>'),
        'collection': ma.AbsoluteURL('books.BookList:get'),
        'notes': ma.AbsoluteURL('books.BookDetail:notes', book_id='<id>')
    })

    class Meta:
        dateformat = 'iso'
        additional = ('id', 'title', 'isbn')

serialize_author = AuthorMarshal.factory(strict=True)
serialize_book = BookMarshal.factory(strict=True)

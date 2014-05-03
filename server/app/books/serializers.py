# -*- coding: utf-8 -*-
#
from ..extensions import ma

# Serializers
class BaseBookMarshal(ma.Serializer):
    created = ma.DateTime(attribute='date_created')

    _links = ma.Hyperlinks({
        'self': ma.AbsoluteURL('books.BookDetail:get', id='<id>'),
        'collection': ma.AbsoluteURL('books.BookList:get'),
        'notes': ma.AbsoluteURL('books.BookDetail:notes', book_id='<id>')
    })

    class Meta:
        dateformat = 'iso'
        additional = ('id', 'title', 'isbn')


class AuthorMarshal(ma.Serializer):
    created = ma.DateTime(attribute='date_created')
    books = ma.Nested(BaseBookMarshal, many=True)

    # Implement HATEOAS
    _links = ma.Hyperlinks({
        'self': ma.AbsoluteURL('books.AuthorDetail:get', id='<id>'),
        'update': ma.AbsoluteURL('books.AuthorDetail:put', id='<id>'),
        'collection': ma.AbsoluteURL('books.AuthorList:get'),
    })

    class Meta:
        dateformat = 'iso'
        additional = ('id', 'first', 'last')

class BookMarshal(BaseBookMarshal):
    author = ma.Nested(AuthorMarshal, exclude=('books', ), allow_null=True)


serialize_author = AuthorMarshal.factory(strict=True)
serialize_book = BookMarshal.factory(strict=True)

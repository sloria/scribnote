# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, url_for
from flask.ext.marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    # api_get_or_404,
    # reqparser,
    ModelResource,
    ModelListResource,
    register_class_views,
)
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)

# Serializers

class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    # Implement HATEOAS
    _links = fields.Hyperlinks({
        'self': fields.AbsoluteURL('books.AuthorDetail:get', id='<id>'),
        'update': fields.AbsoluteURL('books.AuthorDetail:put', id='<id>'),
        'collection': fields.AbsoluteURL('books.AuthorList:get'),
    })

    class Meta:
        additional = ('id', 'first', 'last')

class BookMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')
    author = fields.Nested(AuthorMarshal)

    _links = fields.Hyperlinks({
        'self': fields.URL('books.BookDetail:get', id='<id>', _external=True),
        'collection': fields.URL('books.BookList:get', _external=True),
    })

    class Meta:
        additional = ('id', 'title', 'isbn')

# Views

AUTHOR_ARGS = {
    'first': Arg(str, allow_missing=True),
    'last': Arg(str, allow_missing=True)
}

class AuthorDetail(ModelResource):
    route_base = '/authors/'

    BLUEPRINT = 'books'
    MODEL = Author
    SERIALIZER = AuthorMarshal
    NAME = 'author'

    ARGS = AUTHOR_ARGS


class AuthorList(ModelListResource):
    route_base = '/authors/'

    BLUEPRINT = 'books'
    MODEL = Author
    SERIALIZER = AuthorMarshal
    NAME = 'author'

    ARGS = AUTHOR_ARGS

    def get_links(self):
        return {
            'create': url_for('books.AuthorList:get', _external=True),
            'books': url_for('books.BookList:get', _external=True)
        }


class BookDetail(ModelResource):
    route_base = '/books/'
    BLUEPRINT = 'books'
    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'



class BookList(ModelListResource):
    """Return a list of books."""
    route_base = '/books/'
    BLUEPRINT = 'books'
    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'

    ARGS = {
        'title': Arg(str, required=True),
        'author_id': Arg(int, required=True),
    }

    def get_links(self):
        return {
            'create': url_for('books.BookList:post', _external=True),
            'authors': url_for('books.AuthorList:get', _external=True),
        }


register_class_views(
    [
        AuthorDetail,
        AuthorList,
        BookDetail,
        BookList
    ],
    blueprint
)

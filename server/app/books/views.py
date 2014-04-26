# -*- coding: utf-8 -*-
import logging

from flask import Blueprint
from flask.ext.marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    # api_get_or_404,
    # reqparser,
    ModelResource,
    ModelListResource,
    register_api_views,
)
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)

# Serializers

class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    # Implement HATEOAS
    _links = fields.Hyperlinks({
        'self': fields.URL('books.AuthorResource:get', id='<id>', _external=True),
        'collection': fields.URL('books.AuthorListResource:get', _external=True),
    })

    class Meta:
        additional = ('first', 'last')

class BookMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')
    author = fields.Nested(AuthorMarshal)

    _links = fields.Hyperlinks({
        'self': fields.URL('books.BookResource:get', id='<id>', _external=True),
        'collection': fields.URL('books.BookListResource:get', _external=True),
    })

    class Meta:
        additional = ('title', 'isbn')

# Views

class AuthorResource(ModelResource):
    route_base = '/authors/'

    MODEL = Author
    SERIALIZER = AuthorMarshal
    NAME = 'author'


class AuthorListResource(ModelListResource):
    route_base = '/authors/'

    MODEL = Author
    SERIALIZER = AuthorMarshal
    NAME = 'author'

    ARGS = {
        'first': Arg(str, required=True),
        'last': Arg(str, required=True),
    }


class BookResource(ModelResource):
    route_base = '/books/'
    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'


class BookListResource(ModelListResource):
    route_base = '/books/'

    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'

    ARGS = {
        'title': Arg(str, required=True),
        'author_id': Arg(int, required=True),
    }


register_api_views(
    [
        AuthorResource,
        AuthorListResource,
        BookResource,
        BookListResource
    ],
    blueprint
)

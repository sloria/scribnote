# -*- coding: utf-8 -*-
import httplib as http
import logging

from flask import Blueprint
from flask.ext.restful import Api, Resource
from marshmallow import Serializer, fields
from webargs import Arg

from ..utils.api import (
    api_get_or_404,
    reqparser,
    HyperlinksField,
    ModelResource,
    ModelListResource
)
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)
api = Api(blueprint)

# Serializers

class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    _links = HyperlinksField({
        'self': {
            'endpoint': 'books.author', 'params': {'id': 'id'}
        },
        'collection': {
            'endpoint': 'books.authors',
        }
    })

    class Meta:
        additional = ('first', 'last')

class BookMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')
    author = fields.Nested(AuthorMarshal)
    _links = HyperlinksField({
        'self': {'endpoint': 'books.book', 'params': {'id': 'id'}},
        'collection': {'endpoint': 'books.books'}
    })

    class Meta:
        additional = ('title', 'isbn')

# Views

class AuthorResource(ModelResource):
    MODEL = Author
    SERIALIZER =AuthorMarshal
    NAME = 'author'


class AuthorListResource(ModelListResource):
    MODEL = Author
    SERIALIZER =AuthorMarshal
    NAME = 'author'

    ARGS = {
        'first': Arg(str, required=True),
        'last': Arg(str, required=True),
    }

class BookResource(ModelResource):
    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'

class BookListResource(ModelListResource):

    MODEL = Book
    SERIALIZER = BookMarshal
    NAME = 'book'


api.add_resource(AuthorResource, '/authors/<int:id>', endpoint='author')
api.add_resource(AuthorListResource, '/authors/', endpoint='authors')

api.add_resource(BookResource, '/books/<int:id>', endpoint='book')
api.add_resource(BookListResource, '/books/', endpoint='books')

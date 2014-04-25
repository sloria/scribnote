# -*- coding: utf-8 -*-
import logging

from flask import Blueprint
from flask.ext.restful import Api
from marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    api_get_or_404,
    reqparser,
    Hyperlinks,
    URL,
    ModelResource,
    ModelListResource,
)
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)
api = Api(blueprint)

# Serializers

class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    # Implement HATEOAS
    _links = Hyperlinks({
        'self': URL('books.author', id='<<id>>', _external=True),
        'collection': URL('books.authors', _external=True),
    })

    class Meta:
        additional = ('first', 'last')

class BookMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')
    author = fields.Nested(AuthorMarshal)

    _links = Hyperlinks({
        'self': URL('books.book', id='<<id>>', _external=True),
        'collection': URL('books.books', _external=True),
    })

    class Meta:
        additional = ('title', 'isbn')

# Views

class AuthorResource(ModelResource):
    MODEL = Author
    SERIALIZER = AuthorMarshal
    NAME = 'author'


class AuthorListResource(ModelListResource):
    MODEL = Author
    SERIALIZER = AuthorMarshal
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

    ARGS = {
        'title': Arg(str, required=True),
        'author_id': Arg(int, required=True),
    }


api.add_resource(AuthorResource, '/authors/<int:id>', endpoint='author')
api.add_resource(AuthorListResource, '/authors/', endpoint='authors')

api.add_resource(BookResource, '/books/<int:id>', endpoint='book')
api.add_resource(BookListResource, '/books/', endpoint='books')

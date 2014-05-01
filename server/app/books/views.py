# -*- coding: utf-8 -*-
import logging
import httplib as http

from flask import Blueprint, url_for, request
from flask.ext.marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    # reqparser,
    ModelResource,
    ModelListResource,
    register_class_views,
)
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)

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

    def _get_links(self):
        return {
            'create': url_for('books.AuthorList:get', _external=True),
            'books': url_for('books.BookList:get', _external=True)
        }

    def get(self):
        if request.args.get('all'):
            authors = Author.query.all()
        else:
            authors = Author.query.filter(Author.books.any()).all()
        resp = {
            'result': self.SERIALIZER(authors, many=True).data,
        }
        resp.update({'_links': self._get_links()})
        return resp, http.OK



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
        'author_id': Arg(int, required=False),
        'author_first': Arg(str),
        'author_last': Arg(str),
    }

    def _get_links(self):
        return {
            'create': url_for('books.BookList:post', _external=True),
            'authors': url_for('books.AuthorList:get', _external=True),
        }

    def post(self):
        args = self._parse_request()
        if args['author_id']:
            author = Author.api_get_or_404(args['author_id'])
        elif args['author_first'] or args['author_last']:
            author, created = Author.get_or_create(
                first=args['author_first'],
                last=args['author_last']
            )
        else:
            author = None
        new_book = self.MODEL(title=args['title'], author=author)
        new_book.save()
        return {
            'result': self._serialize(new_book),
            'message': 'Successfully created new book',
        }, http.CREATED


register_class_views(
    [
        AuthorDetail,
        AuthorList,
        BookDetail,
        BookList
    ],
    blueprint
)

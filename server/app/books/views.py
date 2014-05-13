# -*- coding: utf-8 -*-
import logging
import httplib as http

from flask import Blueprint, url_for, request, g
from flask.ext.classy import route
from flask.ext.api.exceptions import NotFound
from webargs import Arg

from ..extensions import auth
from ..meta.api import (
    # reqparser,
    ModelResource,
    ModelListResource,
    register_class_views,
    reqparser,
    use_args,
    APIView,
)
from ..notes.models import Note
from .serializers import serialize_author, serialize_book
from ..notes.serializers import serialize_note
from ..users.serializers import serialize_user
from .models import Author, Book

logger = logging.getLogger(__name__)
blueprint = Blueprint('books', __name__)

# Views

AUTHOR_ARGS = {
    'first': Arg(str, allow_missing=True),
    'last': Arg(str, allow_missing=True)
}

class AuthorDetail(ModelResource):
    route_base = '/authors/'

    BLUEPRINT = 'books'
    MODEL = Author
    SERIALIZER = serialize_author
    NAME = 'author'

    ARGS = AUTHOR_ARGS


class AuthorList(ModelListResource):
    route_base = '/authors/'

    BLUEPRINT = 'books'
    MODEL = Author
    SERIALIZER = serialize_author
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
    SERIALIZER = serialize_book
    NAME = 'book'

    # Nested book/note views

    @route('/<book_id>/notes/')
    def notes(self, book_id):
        book = Book.api_get_or_404(book_id)
        return {
            'result': serialize_note(book.notes, many=True).data
        }

    @route('/<book_id>/notes/<note_id>')
    def note(self, book_id, note_id):
        note = Note.api_get_or_404(note_id)
        return {
            'result': serialize_note(note).data
        }

    @route('/<book_id>/notes/<note_id>', methods=['PUT'])
    @use_args({
        'text':    Arg(unicode, allow_missing=True,
                        validate=lambda t: t and len(t) > 0),
        'book_id': Arg(int, allow_missing=True),
    })
    def note_edit(self, reqargs, book_id, note_id):
        note = Note.api_get_or_404(note_id)
        note.update(**reqargs)
        note.save()
        return {
            'result': serialize_note(note).data
        }

    @route('/<book_id>/notes/<note_id>', methods=['DELETE'])
    def note_delete(self, book_id, note_id):
        note = Note.api_get_or_404(note_id)
        note.delete(commit=True)
        return {}


class BookList(ModelListResource):
    """Return a list of books."""
    route_base = '/books/'
    BLUEPRINT = 'books'
    MODEL = Book
    SERIALIZER = serialize_book
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


class ReadingList(APIView):
    route_base = '/reading/'
    decorators = [auth.login_required]

    ARGS = {
        'book_id': Arg(int, required=True)
    }

    def get(self):
        current_user = g.user
        reading_list = current_user.reading_list.all()
        res = {
            'result': serialize_book(reading_list, many=True).data,
            'user': serialize_user(current_user).data
        }
        return res

    def post(self):
        current_user = g.user
        reqargs = self._parse_request()
        book = Book.get_by_id(reqargs['book_id'])
        if not book:
            raise NotFound(detail='Book with id {0!r} not found.'.format(book.id))
        current_user.add_to_reading_list(book)
        current_user.save()
        return {
            'result': serialize_book(book).data,
            'user': serialize_user(current_user).data,
        }, http.OK

    def put(self):
        current_user = g.user
        reqargs = self._parse_request()
        book = Book.get_by_id(reqargs['book_id'])
        if not book:
            raise NotFound(detail='Book with id {0!r} not found.'.format(book.id))
        current_user.toggle_read(book)
        current_user.save()
        has_read = current_user.has_read(book)
        return {
            'result': serialize_book(book, extra={'read': has_read}).data,
            'user': serialize_user(current_user).data,
        }, http.OK

register_class_views(
    [
        AuthorDetail,
        AuthorList,
        BookDetail,
        BookList,
        ReadingList,
    ],
    blueprint
)

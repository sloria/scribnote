# -*- coding: utf-8 -*-
import logging
import httplib as http

from flask import Blueprint, url_for, request
from webargs import Arg

from ..meta.api import (
    # reqparser,
    ModelResource,
    ModelListResource,
    register_class_views,
    reqparser,
    use_args
)
from ..notes.models import Note
from ..serializers import serialize_author, serialize_book, serialize_note
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


register_class_views(
    [
        AuthorDetail,
        AuthorList,
        BookDetail,
        BookList
    ],
    blueprint
)

##### Nested routes ######

route = blueprint.route

@route('/books/<book_id>/notes/')
def notes(book_id):
    book = Book.api_get_or_404(book_id)
    return {
        'result': serialize_note(book.notes, many=True).data
    }

@route('/books/<book_id>/notes/<note_id>')
def note(book_id, note_id):
    note = Note.api_get_or_404(note_id)
    return {
        'result': serialize_note(note).data
    }


NOTE_ARGS = {
    'text': Arg(unicode, allow_missing=True),
    'book_id': Arg(int, allow_missing=True),
}

@route('/books/<book_id>/notes/<note_id>', methods=['PUT'])
@use_args(NOTE_ARGS)
def note_edit(reqargs, book_id, note_id):
    note = Note.api_get_or_404(note_id)
    note.update(**reqargs)
    note.save()
    return {
        'result': serialize_note(note).data
    }

# -*- coding: utf-8 -*-
import logging
import httplib as http

from flask import Blueprint
from webargs import Arg

from ..meta.api import (
    ModelResource,
    ModelListResource,
    register_class_views,
)
from ..books.models import Book
from ..serializers import NoteMarshal
from .models import Note


logger = logging.getLogger(__name__)

blueprint = Blueprint('notes', __name__)

NOTE_ARGS = {
    'text': Arg(unicode, allow_missing=True),
    'book_id': Arg(int, allow_missing=True)
}

class NoteResource(object):
    route_base = '/notes/'
    BLUEPRINT = 'notes'
    MODEL = Note
    SERIALIZER = NoteMarshal

class NoteDetail(NoteResource, ModelResource):
    """Generic view set for the note detail endpoint.
    """
    ARGS = NOTE_ARGS

class NoteList(NoteResource, ModelListResource):
    """Generic set of views for the note list endpoint.
    """
    ARGS = NOTE_ARGS

    def post(self):
        args = self._parse_request()
        book = Book.api_get_or_404(args['book_id'])
        new_note = Note.create(text=args['text'], book=book)
        result = {
            'result': self._serialize(new_note)
        }
        return result, http.CREATED


register_class_views(
    [
        NoteList,
        NoteDetail,
    ],
    blueprint
)

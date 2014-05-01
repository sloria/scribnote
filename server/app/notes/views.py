# -*- coding: utf-8 -*-
import logging
import httplib as http

from flask import Blueprint
from flask.ext.marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    ModelResource,
    ModelListResource,
    register_class_views,
)
from ..books.models import Book
from .models import Note


logger = logging.getLogger(__name__)

blueprint = Blueprint('notes', __name__)


# Serializers

class NoteMarshal(Serializer):
    class Meta:
        additional = ('text', )
    created = fields.DateTime(attribute='date_created')
    _links = fields.Hyperlinks({
        'collection': fields.URL('notes.NoteList:get'),
    })

serialize_note = NoteMarshal.factory(strict=True)

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


@blueprint.route('/books/<int:book_id>/notes/')
def book_note_list(book_id):
    book = Book.api_get_or_404(book_id)
    return {
        'result': serialize_note(book.notes, many=True).data
    }


register_class_views(
    [
        NoteList,
        NoteDetail,
    ],
    blueprint
)

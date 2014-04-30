# -*- coding: utf-8 -*-
import logging

from flask import Blueprint
from flask.ext.marshmallow import Serializer, fields
from webargs import Arg

from ..meta.api import (
    ModelResource,
    ModelListResource,
    register_class_views,
)
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


NOTE_ARGS = {
    'text': Arg(unicode, target='json')
}

class NoteResource(object):
    route_base = '/notes/'
    BLUEPRINT = 'notes'
    MODEL = Note
    SERIALIZER = NoteMarshal

class NoteDetail(NoteResource, ModelResource):
    ARGS = NOTE_ARGS

class NoteList(NoteResource, ModelListResource):
    ARGS = NOTE_ARGS

register_class_views(
    [
        NoteList,
        NoteDetail,
    ],
    blueprint
)

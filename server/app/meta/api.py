# -*- coding: utf-8 -*-
"""Utlities for the REST API. Includes utilites for request argument parsing,
marshalling, etc.
"""
import httplib as http

from flask import request
from flask.ext.classy import FlaskView
from flask.ext.api.exceptions import NotFound, APIException
from webargs import core
from webargs.flaskparser import FlaskParser


class BadRequestError(APIException):
    status_code = 400
    detail = 'Bad request.'

class FlaskAPIParser(FlaskParser):
    """Custom request argument parser from the webargs library that
    handles API errors by raising Flask-API's APIException.
    """
    TARGET_MAP = {
        'json': 'parse_json',
        'querystring': 'parse_querystring',
        'form': 'parse_form',
        'headers': 'parse_headers',
        'cookies': 'parse_cookies',
        'files': 'parse_files',
        'data': 'parse_data',
    }

    def parse_data(self, req, name, arg):
        return core.get_value(req.data, name, arg.multiple)

    def handle_error(self, error):
        raise BadRequestError(str(error))

reqparser = FlaskAPIParser()
use_kwargs = reqparser.use_kwargs
use_args = reqparser.use_args


class ModelResource(FlaskView):
    """Implements generic HTTP-based CRUD for a given model.
    Must define ``MODEL`` and ``SERIALIZER`` class variables.
    """
    MODEL = None
    SERIALIZER = None
    NAME = None

    def get(self, id):
        """Return a single instance."""
        name = getattr(self, 'NAME', 'Resource')
        obj = api_get_or_404(self.MODEL, id,
            error_msg="{name} not found".format(name=name))
        return {
            'result': self.SERIALIZER(obj, strict=True).data,
        }, http.OK


class ModelListResource(FlaskView):
    """Implements generic HTTP-based collection CRUD for a given model."""

    MODEL = None
    SERIALIZER = None
    NAME = None
    ARGS = None

    def get(self):
        """Return a list of the requested objects."""
        objects = self.MODEL.query.all()
        return {
            'result': self.SERIALIZER(objects, many=True).data
        }, http.OK

    def post(self):
        """Create a new instance of the resource."""
        if self.ARGS:
            args = reqparser.parse(self.ARGS, request, targets=('data', 'json'))
        else:
            args = {}
        new_obj = self.MODEL.create(**args)
        name = getattr(self, 'NAME', 'object')
        return {
            'result': self.SERIALIZER(new_obj, strict=True).data,
            'message': 'Successfully created new {0}'.format(name)
        }, http.CREATED


def api_get_or_404(model, id, error_msg=None):
    """Get a model by its primary key; abort with 404 using Flask-RESTful's
    abort helper.
    """
    obj = model.query.get(id)
    if not obj:
        raise NotFound(detail=error_msg)
    return obj


def register_class_views(view_classes, app, route_base=None, route_prefix=None):
    for each in view_classes:
        each.register(app, route_base=route_base, route_prefix=route_prefix)

def register_api_views(view_classes, app, route_prefix='/api/'):
    register_class_views(view_classes, app, route_prefix=route_prefix)

# -*- coding: utf-8 -*-
"""Utlities for the REST API. Includes utilites for request argument parsing,
marshalling, etc.
"""
import httplib as http

from flask import request, url_for
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
        try:
            return core.get_value(req.data, name, arg.multiple)
        except AttributeError:
            return None

    def handle_error(self, error):
        raise BadRequestError(str(error))

reqparser = FlaskAPIParser()
use_kwargs = reqparser.use_kwargs
use_args = reqparser.use_args

class APIView(FlaskView):
    """An abstract APIView."""

    ARGS = None
    MODEL = None
    SERIALIZER = None
    NAME = None
    BLUEPRINT = None

    def parse_request(self):
        if self.ARGS:
            args = reqparser.parse(self.ARGS, request, targets=('data', 'json'))
        else:
            args = {}
        return args

    def serialize(self, obj, **kwargs):
        return self.SERIALIZER(obj, **kwargs).data

    def get_name(self):
        return getattr(self, 'NAME', 'object')

    def get_links(self):
        return {}

    def post_links(self):
        return {}

    def put_links(self):
        return {}


class ModelResource(APIView):
    """Implements generic HTTP-based CRUD for a given model.
    Must define ``MODEL`` and ``SERIALIZER`` class variables.
    """

    def get(self, id):
        """Return a single instance."""
        name = getattr(self, 'NAME', 'Resource')
        obj = api_get_or_404(self.MODEL, id,
            error_msg="{name} not found".format(name=name))
        res = {
            'result': self.SERIALIZER(obj, strict=True).data,
        }
        res.update(self.get_links())
        return res, http.OK

    def put(self, id):
        obj = api_get_or_404(self.MODEL, id)
        attrs = self.parse_request()
        obj.update(**attrs)
        obj.save()
        res = {
            'result': self.SERIALIZER(obj, strict=True).data,
            'message': 'Updated {0}'.format(self.get_name())
        }
        res.update({
            '_links': self.put_links(),
        })
        return res, http.OK


class ModelListResource(APIView):
    """Implements generic HTTP-based collection CRUD for a given model."""


    def get(self):
        """Return a list of the requested objects."""
        objects = self.MODEL.query.all()
        assert self.BLUEPRINT is not None, 'Must define BLUEPRINT'
        res = {
            'result': self.SERIALIZER(objects, many=True).data,
        }
        res.update({
            '_links': self.get_links(),
        })
        return res, http.OK

    def post(self):
        """Create a new instance of the resource."""
        args = self.parse_request()
        new_obj = self.MODEL.create(**args)
        name = self.get_name()
        res = {
            'result': self.SERIALIZER(new_obj, strict=True).data,
            'message': 'Successfully created new {0}'.format(name)
        }
        res.update({
            '_links': self.post_links(),
        })
        return res, http.CREATED


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

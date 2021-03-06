# -*- coding: utf-8 -*-
"""Utlities for the REST API. Includes utilites for request argument parsing,
marshalling, etc.
"""
import httplib as http

from flask import request
from flask.ext.classy import FlaskView
from flask.ext.api.exceptions import APIException
from webargs import core
from webargs.flaskparser import FlaskParser


class BadRequestError(APIException):
    status_code = 400
    detail = 'Bad request.'

class FlaskAPIParser(FlaskParser):
    """Custom request argument parser from the webargs library that
    handles API errors by raising Flask-API's APIException.
    """

    def parse_data(self, req, name, arg):
        try:
            return core.get_value(req.data, name, arg.multiple)
        except AttributeError:
            return None

    def handle_error(self, error):
        raise BadRequestError(str(error))

# Register custom parse_data method for the 'data' target
FlaskAPIParser.TARGET_MAP['data'] = 'parse_data'
# Add 'data' to default targets to parse
FlaskAPIParser.DEFAULT_TARGETS = ('data', 'json', 'querystring')

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

    def _parse_request(self):
        if self.ARGS:
            args = reqparser.parse(self.ARGS, request, targets=('data', 'json'))
        else:
            args = {}
        return args

    def _serialize(self, obj, **kwargs):
        return self.SERIALIZER(obj, **kwargs).data

    def _get_name(self):
        return getattr(self, 'NAME', 'object')

    def _get_links(self):
        return {}

    def _post_links(self):
        return {}

    def _put_links(self):
        return {}


class ModelResource(APIView):
    """Implements generic HTTP-based CRUD for a given model.
    Must define ``MODEL`` and ``SERIALIZER`` class variables.
    """

    def get(self, id):
        """Return a single instance."""
        name = getattr(self, 'NAME', 'Resource')
        obj = self.MODEL.api_get_or_404(id,
            error_msg="{name} not found".format(name=name))
        res = {
            'result': self._serialize(obj, strict=True),
        }
        res.update(self._get_links())
        return res, http.OK

    def put(self, id):
        obj = self.MODEL.api_get_or_404(id)
        attrs = self._parse_request()
        obj.update(**attrs)
        obj.save()
        res = {
            'result': self.SERIALIZER(obj, strict=True).data,
            'message': 'Updated {0}'.format(self._get_name())
        }
        res.update({
            '_links': self._put_links(),
        })
        return res, http.OK

    def delete(self, id):
        name = getattr(self, 'NAME', 'Resource')
        obj = self.MODEL.api_get_or_404(id,
            error_msg="{name} not found".format(name=name))
        obj.delete(commit=True)
        return {}


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
            '_links': self._get_links(),
        })
        return res, http.OK

    def post(self):
        """Create a new instance of the resource."""
        args = self._parse_request()
        new_obj = self.MODEL.create(**args)
        name = self._get_name()
        res = {
            'result': self.SERIALIZER(new_obj, strict=True).data,
            'message': 'Successfully created new {0}'.format(name)
        }
        res.update({
            '_links': self._post_links(),
        })
        return res, http.CREATED


def register_class_views(view_classes, app, route_base=None, route_prefix=None):
    """Registers a list of FlaskViews to an app or blueprint. ::

        register_class_views([
            UserDetail, UserList,
            TweetDetail, TweetList
        ], blueprint)

    """
    for each in view_classes:
        each.register(app, route_base=route_base, route_prefix=route_prefix)

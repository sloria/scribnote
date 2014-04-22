# -*- coding: utf-8 -*-
"""Utlities for the REST API. Includes utilites for request argument parsing,
marshalling, etc.
"""
import httplib as http

from flask import url_for, request
from webargs.flaskparser import FlaskParser
from marshmallow import fields

from flask.ext.restful import abort as api_abort, Resource


class FlaskAPIParser(FlaskParser):
    """Custom request argument parser from the webargs library that
    handles API errors with flask-restful's ``abort`` function instead
    of flask's abort function.
    """
    def handle_error(self, error):
        api_abort(400, message=str(error))

reqparser = FlaskAPIParser()
use_kwargs = reqparser.use_kwargs
use_args = reqparser.use_args


class ModelResource(Resource):
    """Implements HTTP-based CRUD for a given model. Must define ``MODEL`` and
    ``SERIALIZER`` class variables.
    """
    MODEL = None
    SERIALIZER = None
    NAME = None

    def get(self, id):
        """Return a single instance."""
        name = getattr(self, 'NAME', 'Resource')
        obj = api_get_or_404(self.MODEL, id,
            message="{name} not found".format(name=name))
        return {
            'result': self.SERIALIZER(obj).data,
        }, http.OK


class ModelListResource(Resource):
    """Implements HTTP-based collection CRUD for a given model."""

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
        args = reqparser.parse(self.ARGS, request)
        new_obj = self.MODEL.create(**args)
        name = getattr(self, 'NAME', 'object')
        return {
            'result': self.SERIALIZER(new_obj).data,
            'message': 'Successfully created new {0}'.format(name)
        }, http.CREATED


def api_get_or_404(model, id, **kwargs):
    """Get a model by its primary key; abort with 404 using Flask-RESTful's
    abort helper.
    """
    return model.query.get(id) or api_abort(404, **kwargs)


class HyperlinksField(fields.Raw):
    """Custom marshmallow field for that outputs a dictionary of hyperlinks,
    given a dictionary schema.

    Example: ::

        _links = HyperlinksField({
            'self': {
                'endpoint': 'author', 'params': {'id': 'id'}
            },
            'collection': {
                'endpoint': 'author_list',
            }
        })

    :param dict schema: A dict that maps endpoint names to an endpoint and params.
        The ``endpoint`` key is the Flask endpoint and ``params`` are the parameters
        passed to ``Flask.url_for``.
    """

    def __init__(self, schema, **kwargs):
        super(HyperlinksField, self).__init__(**kwargs)
        self.schema = schema

    def _get_url(self, config, obj):
        param_values = {}
        endpoint = config['endpoint']
        for name, attr in config.get('params', {}).iteritems():
            try:
                param_values[name] = self.get_value(key=attr, obj=obj)
            except AttributeError:
                param_values[name] = attr
        return url_for(endpoint, **param_values)

    def output(self, key, obj):
        ret = {}
        for key, config in self.schema.iteritems():
            ret[key] = self._get_url(config, obj)
        return ret

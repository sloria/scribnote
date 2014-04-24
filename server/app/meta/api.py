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
            message="{name} not found".format(name=name))
        return {
            'result': self.SERIALIZER(obj).data,
        }, http.OK


class ModelListResource(Resource):
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

class Link(fields.Raw):
    """A hyperlink to an endpoint.

    Provides sugar for the HyperlinksField.

    ``Link('books', id='_id', _external=True)``
    """

    def __init__(self, endpoint, attribute=None, **kwargs):
        self.endpoint = endpoint
        self.params = kwargs
        self.attribute = attribute

    def output(self, key, obj):
        param_values = {}
        for name, attr in self.params.iteritems():
            try:
                param_values[name] = self.get_value(key=attr, obj=obj)
            except AttributeError:
                param_values[name] = attr
        return url_for(self.endpoint, **param_values)


def rapply(d, func, *args, **kwargs):
    """Apply a function to a all values in a dictionary, recursively."""
    if isinstance(d, dict):
        return {
            key: rapply(value, func, **kwargs)
            for key, value in d.iteritems()
        }
    else:
        return func(d, **kwargs)


def _url_val(val, key, obj, **kwargs):
    """Function applied by HyperlinksField to get the correct value in the
    schema.
    """
    if isinstance(val, Link):
        return val.output(key, obj, **kwargs)
    else:
        return val


class HyperlinksField(fields.Raw):
    """Custom marshmallow field that outputs a dictionary of hyperlinks,
    given a dictionary schema.

    Example: ::

        _links = HyperlinksField({
            'self': Link('author', id='id'),
            'collection': Link('author_list'),
            }
        })

    :param dict schema: A dict that maps endpoint names to an endpoint and params.
        The ``endpoint`` key is the Flask endpoint and ``params`` are the parameters
        passed to ``Flask.url_for``.
    """

    def __init__(self, schema, **kwargs):
        super(HyperlinksField, self).__init__(**kwargs)
        self.schema = schema

    def output(self, key, obj):
        return rapply(self.schema, _url_val, key=key, obj=obj)
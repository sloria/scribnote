# -*- coding: utf-8 -*-
"""Utlities for the REST API. Includes utilites for request argument parsing,
marshalling, etc.
"""
import httplib as http
import re

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

##### marshmallow

_tpl_pattern = re.compile(r'\s*<<\s*(\S*)\s*>>\s*')

def tpl(val):
    match = _tpl_pattern.match(val)
    if match:
        return match.groups()[0]
    return None


class Url(fields.Raw):
    """A hyperlink to an endpoint.

    Usage: ::

        url = Url('author_get', id='<<id>>')
        absolute_url = Url('author_get', id='<<id>>', _external=True)

    :param str endpoint: Flask endpoint name.
    :param kwargs: Same keyword arguments as Flask's url_for, except string
        arguments enclosed in `<< >>` will be interpreted as attributes to pull
        from the object.
    """

    def __init__(self, endpoint, **kwargs):
        self.endpoint = endpoint
        self.params = kwargs
        # All fields need self.attribute
        self.attribute = None

    def output(self, key, obj):
        param_values = {}
        for name, attr in self.params.iteritems():
            try:
                param_values[name] = self.get_value(key=tpl(str(attr)), obj=obj)
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
    if isinstance(val, Url):
        return val.output(key, obj, **kwargs)
    else:
        return val


class Hyperlinks(fields.Raw):
    """Custom marshmallow field that outputs a dictionary of hyperlinks,
    given a dictionary schema with ``Url`` objects as values.

    Example: ::

        _links = Hyperlinks({
            'self': Url('author', id='id'),
            'collection': Url('author_list'),
            }
        })

    ``Url`` objects can be nested within the dictionary. ::

        _links = Hyperlinks({
            'self': {
                'href': Url('book', id=<<id>>),
                'title': 'book detail'
            }
        })

    :param dict schema: A dict that maps endpoint names to an endpoint and params.
        The ``endpoint`` key is the Flask endpoint and ``params`` are the parameters
        passed to ``Flask.url_for``.
    """

    def __init__(self, schema, **kwargs):
        super(Hyperlinks, self).__init__(**kwargs)
        self.schema = schema

    def output(self, key, obj):
        return rapply(self.schema, _url_val, key=key, obj=obj)

# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
import logging
from flask import make_response
from flask.ext.api import FlaskAPI

from .settings import ProdConfig
from .extensions import register_extensions
from . import main, books, notes, users

logger = logging.getLogger(__name__)


def create_app(config_object=ProdConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    api = FlaskAPI('scribnote_api', static_folder='../client/app/')
    api.config.from_object(config_object)
    register_extensions(api)
    register_blueprints(api)

    # Make api cross-domain accessible
    @api.after_request
    def after_request(data):
        resp = make_response(data)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-RequestedWith,Content-Type,Accept,Authorization'
        resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE'
        resp.headers['Access-Control-Max-Age'] = '604800'
        return resp
    return api

def register_blueprints(app):
    api_blueprints = [
        books.views.blueprint,
        main.views.blueprint,
        notes.views.blueprint,
        users.views.blueprint,
    ]
    for bp in api_blueprints:
        app.register_blueprint(
            bp,
            url_prefix='/api'
        )
    # app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    return None

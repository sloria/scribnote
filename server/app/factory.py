# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
import logging
from flask import Flask, make_response
from flask.ext.api import FlaskAPI
from werkzeug.wsgi import DispatcherMiddleware

from .settings import ProdConfig
from .extensions import (
    bcrypt,
    cache,
    db,
    login_manager,
    migrate,
    api_manager,
)
from . import main, books

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

    @api.after_request
    def after_request(data):
        resp = make_response(data)
        resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-RequestedWith,Content-Type,Accept'
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return api


def register_extensions(app):
    api_manager.init_app(app, flask_sqlalchemy_db=db)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    api_blueprints = [
        books.views.blueprint,
        main.views.blueprint,
    ]
    for bp in api_blueprints:
        app.register_blueprint(
            bp,
            # url_prefix='/api'
        )
    # app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    return None

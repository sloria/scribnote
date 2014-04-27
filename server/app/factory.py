# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
import logging
from flask import Flask
from flask.ext.api import FlaskAPI

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
    app = FlaskAPI('commonplace')
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app


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
            url_prefix='/api'
        )
    # app.register_blueprint(public.views.blueprint)
    # app.register_blueprint(user.views.blueprint)
    return None

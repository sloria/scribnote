# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""
import logging

logger = logging.getLogger(__name__)

from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt()

from flask.ext.login import LoginManager
login_manager = LoginManager()

from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from flask.ext.migrate import Migrate
migrate = Migrate()

from flask.ext.cache import Cache
cache = Cache()

from flask.ext.marshmallow import Marshmallow
ma = Marshmallow()


ALL_EXTENSIONS = [
    bcrypt,
    login_manager,
    db,
    migrate,
    cache,
    ma
]


def register_extensions(app):
    """Register all extensions on the app."""
    for ext in ALL_EXTENSIONS:
        logger.debug('Registering extension:')
        logger.debug(ext)
        if isinstance(ext, Migrate):
            ext.init_app(app, db)
        else:
            ext.init_app(app)

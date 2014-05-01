#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script used for database operations. For all other
tasks, use invoke.
"""
import os
from flask.ext.script import Manager, Shell
from flask.ext.migrate import MigrateCommand

from app.factory import create_app
from app.settings import DevConfig, ProdConfig

if os.environ.get("PSYGIST_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

def _make_context():
    from app.books.models import Author, Book
    from app.notes.models import Note
    from app.user.models import User
    from app.meta.database import db
    from flask import url_for, current_app
    from tests.utils import fake
    app = current_app
    return locals()

manager = Manager(app)
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

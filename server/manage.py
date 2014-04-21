#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Management script used for database operations. For all other
tasks, use invoke.
"""
import os
from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from app.factory import create_app
from app.settings import DevConfig, ProdConfig

if os.environ.get("PSYGIST_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# -*- coding: utf-8 -*-
"""Server app invoke tasks."""
import os

import pip
from invoke import task, run


HERE = os.path.abspath(os.path.dirname(__file__))
MANAGE_SCRIPT = os.path.join(HERE, 'manage.py')

def get_app():
    # Import inside the function so that invoke will work before dependencies
    # are installed
    from app.factory import create_app
    from app.settings import DevConfig, ProdConfig
    if os.environ.get("SCRIBNOTE_ENV") == 'prod':
        app = create_app(ProdConfig)
    else:
        app = create_app(DevConfig)
    return app


@task(default=True)
def serve(port=5000):
    app = get_app()
    app.run(port=5000)

@task
def requirements(dev=False):
    """Install python requirements with pip."""
    if dev:
        reqfile = os.path.join(HERE, 'requirements', 'dev.txt')
    else:
        reqfile = os.path.join(HERE, 'requirements', 'prod.txt')
    pip.main(['install', '--upgrade', '-r', reqfile])

@task
def shell():
    """Start up the enhanced shell with all models automatically imported."""
    run('python {0} shell'.format(MANAGE_SCRIPT), pty=True)

@task
def initdb():
    """Initialize the database."""
    run(
        'python {0} db && python {0} migrate && python {0} upgrade'.format(MANAGE_SCRIPT),
        pty=True
    )

@task
def migrate():
    """Generate a migration script."""
    run('python {0} db migrate'.format(MANAGE_SCRIPT), pty=True)


@task('migrate')
def automigrate():
    """Generate a migration script and upgrade the database."""
    run('python {0} db upgrade'.format(MANAGE_SCRIPT), pty=True)

@task
def test():
    """Run all the tests in the tests directory."""
    import pytest
    pytest.main([os.path.join(HERE, 'tests'), '-s'])

# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from server.app.settings import TestConfig
from server.app.factory import create_app
from server.app.database import db as _db

from .factories import UserFactory

@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()

@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.drop_all()

@pytest.fixture(scope='session')
def wt(app):
    return TestApp(app)


@pytest.fixture
def user(db):
    return UserFactory()

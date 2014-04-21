# -*- coding: utf-8 -*-

import pytest
from flask import url_for
from marshmallow.utils import rfcformat

from server.app.books.models import Author
from .factories import AuthorFactory


@pytest.mark.usefixtures('db')
class TestAuthorResource:

    def test_url(self, app):
        assert url_for('books.author', id=123) == '/api/v1/authors/123'

    def test_get(self, wt):
        author = AuthorFactory()
        url = url_for('books.author', id=author.id)
        res = wt.get(url)
        assert res.status_code == 200
        data = res.json['result']
        assert data['first'] == author.first
        assert data['last'] == author.last
        assert data['created'] == rfcformat(author.date_created)

    def test_get_if_author_doesnt_exist(self, wt):
        url = url_for("books.author", id=123)
        res = wt.get(url, expect_errors=True)
        assert res.status_code == 404
        assert res.json['message'] == 'Author not found'

@pytest.mark.usefixtures('db')
class TestAuthorListResource:

    @pytest.fixture
    def url(self, app):
        """The URL for the author list resource."""
        return url_for('books.author_list')

    def test_url(self, url):
        assert url == '/api/v1/authors/'

    def test_get(self, wt, url):
        author1, author2 = AuthorFactory(), AuthorFactory()
        res = wt.get(url)
        assert res.status_code == 200
        data = res.json['result']
        assert len(data) == Author.query.count()

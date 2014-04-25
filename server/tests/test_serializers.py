# -*- coding: utf-8 -*-

import pytest
from marshmallow.utils import rfcformat

from flask import url_for
from marshmallow import pprint

from server.app.books.views import AuthorMarshal, BookMarshal
from .factories import AuthorFactory, BookFactory

@pytest.mark.usefixtures('db')
class TestAuthorMarshal:

    def test_serialize_single(self):
        author = AuthorFactory()
        data = AuthorMarshal(author, strict=True).data
        assert data['first'] == author.first
        assert data['last'] == author.last
        assert data['created'] == rfcformat(author.date_created)

    def test_serialize_single_links(self, app):
        author = AuthorFactory()
        data = AuthorMarshal(author, strict=True).data
        links = data['_links']
        assert links['self'] == url_for('books.author', id=author.id, _external=True)
        assert links['collection'] == url_for('books.authors', _external=True)


@pytest.mark.usefixtures('db')
class TestBookMarshal:

    def test_serialize_single(self):
        book = BookFactory()
        data = BookMarshal(book, strict=True).data
        assert data['created'] == rfcformat(book.date_created)
        assert 'author' in data

    def test_serialize_single_links(self):
        book = BookFactory()
        data = BookMarshal(book, strict=True).data
        links = data['_links']
        assert links['self'] == url_for('books.book', id=book.id, _external=True)
        assert links['collection'] == url_for('books.books', _external=True)

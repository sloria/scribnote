# -*- coding: utf-8 -*-

import pytest
from flask import url_for
import httplib as http
from marshmallow.utils import rfcformat

from server.app.books.models import Author, Book
from .factories import AuthorFactory, BookFactory
from .utils import fake


@pytest.mark.usefixtures('db')
class TestAuthorResource:

    def test_url(self, app):
        assert url_for('books.AuthorResource:get', id=123) == '/api/authors/123'

    def test_get(self, wt):
        author = AuthorFactory()
        url = url_for('books.AuthorResource:get', id=author.id)
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert data['first'] == author.first
        assert data['last'] == author.last
        assert data['created'] == rfcformat(author.date_created)

    def test_get_if_author_doesnt_exist(self, wt):
        url = url_for("books.AuthorResource:get", id=123)
        res = wt.get(url, expect_errors=True)
        assert res.status_code == http.NOT_FOUND
        assert res.json['message'] == 'author not found'

@pytest.mark.usefixtures('db')
class TestAuthorListResource:

    @pytest.fixture
    def url(self, app):
        """The URL for the author list resource."""
        return url_for('books.AuthorListResource:get')

    def test_url(self, url):
        assert url == '/api/authors/'

    def test_get(self, wt, url):
        author1, author2 = AuthorFactory(), AuthorFactory()
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert len(data) == Author.query.count()

    def test_post_creates_author(self, wt, url):
        old_count = Author.query.count()
        first, last = fake.first_name(), fake.last_name()
        res = wt.post_json(url, {'first': first, 'last': last})
        assert res.status_code == http.CREATED
        data = res.json['result']
        assert data['first'] == first
        assert data['last'] == last
        assert res.json['message'] == 'Successfully created new author'
        assert Author.query.count() == old_count + 1
        latest = Author.get_latest()
        assert latest.first == first
        assert latest.last == last

    def test_first_name_required(self, wt, url):
        res = wt.post_json(url, {'last': fake.last_name()}, expect_errors=True)
        assert res.status_code == 400
        # Default webargs error message
        msg = res.json['message']
        assert msg == 'Required parameter {0!r} not found.'.format('first')

    def test_last_name_required(self, wt, url):
        res = wt.post_json(url, {'first': fake.last_name()}, expect_errors=True)
        assert res.status_code == 400
        # Default webargs error message
        msg = res.json['message']
        assert msg == 'Required parameter {0!r} not found.'.format('last')

@pytest.mark.usefixtures('db')
class TestBookResource:

    def test_url(self):
        assert url_for('books.BookResource:get', id=123) == '/api/books/123'

    def test_get(self, wt):
        book = BookFactory()
        url = url_for('books.BookResource:get', id=book.id)
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert data['title'] == book.title
        assert 'author' in data

    def test_post_creates_book(self, wt):
        author = AuthorFactory()
        old_count = Book.query.count()
        first, last = fake.first_name(), fake.last_name()
        url = url_for('books.BookListResource:post')
        title = fake.bs()
        res = wt.post_json(url, {'title': title, 'author_id': author.id})
        assert res.status_code == http.CREATED
        data = res.json['result']
        assert data['title'] == title
        assert res.json['message'] == 'Successfully created new book'
        assert Book.query.count() == old_count + 1
        latest = Book.get_latest()
        assert latest.title == title
        assert latest.author == author

    def test_post_requires_author_id(self, wt):
        url = url_for('books.BookListResource:get')
        title = fake.bs()
        res = wt.post_json(url, {'title': title}, expect_errors=True)
        assert res.status_code == 400

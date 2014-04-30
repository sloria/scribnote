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

    def test_get(self, wt):
        author = AuthorFactory()
        url = url_for('books.AuthorDetail:get', id=author.id)
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert data['first'] == author.first
        assert data['last'] == author.last
        assert data['created'] == rfcformat(author.date_created)
        assert 'books' in data

    def test_get_if_author_doesnt_exist(self, wt):
        url = url_for("books.AuthorDetail:get", id=123)
        res = wt.get(url, expect_errors=True)
        assert res.status_code == http.NOT_FOUND
        assert res.json['message'] == 'author not found'

    def test_put_update_name(self, wt):
        author = AuthorFactory()
        url = url_for('books.AuthorDetail:put', id=author.id)
        new_first, new_last = fake.first_name(), fake.last_name()
        payload = {'first': new_first, 'last': new_last}
        res = wt.put_json(url, payload)
        assert res.status_code == 200
        latest = Author.get_latest()
        # Name was updated
        assert latest.first == new_first
        assert latest.last == new_last

    def test_put_update_first(self, wt):
        a = AuthorFactory()
        url = url_for('books.AuthorDetail:put', id=a.id)
        new_firstname = fake.first_name()
        payload = {'first': new_firstname}
        res = wt.put_json(url, payload)
        assert res.status_code == 200
        assert a.first == new_firstname
        assert a.first is not None

@pytest.mark.usefixtures('db')
class TestAuthorListResource:

    @pytest.fixture
    def url(self, app):
        """The URL for the author list resource."""
        return url_for('books.AuthorList:get')

    def test_get(self, wt, url):
        author1, author2 = AuthorFactory(), AuthorFactory()
        book1, book2 = BookFactory(author=author1), BookFactory(author=author2)
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert len(data) == Author.query.count()
        links = res.json['_links']
        assert 'create' in links
        assert 'books' in links

    def test_get_excludes_authors_with_no_books(self, wt, url):
        author1, author2 = AuthorFactory(), AuthorFactory()
        book1 = BookFactory(author=author1)
        res = wt.get(url)
        assert len(res.json['result']) == 1
        res = wt.get(url + '?all=1')
        assert len(res.json['result']) == 2

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

    # def test_first_name_required(self, wt, url):
    #     res = wt.post_json(url, {'last': fake.last_name()}, expect_errors=True)
    #     assert res.status_code == 400
    #     # Default webargs error message
    #     msg = res.json['message']
    #     assert msg == 'Required parameter {0!r} not found.'.format('first')

    # def test_last_name_required(self, wt, url):
    #     res = wt.post_json(url, {'first': fake.last_name()}, expect_errors=True)
    #     assert res.status_code == 400
    #     # Default webargs error message
    #     msg = res.json['message']
    #     assert msg == 'Required parameter {0!r} not found.'.format('last')

@pytest.mark.usefixtures('db')
class TestBookResource:

    def test_get(self, wt):
        book = BookFactory()
        url = url_for('books.BookDetail:get', id=book.id)
        res = wt.get(url)
        assert res.status_code == http.OK
        data = res.json['result']
        assert data['title'] == book.title
        assert 'author' in data

    def test_post_creates_book(self, wt):
        author = AuthorFactory()
        old_count = Book.query.count()
        url = url_for('books.BookList:post')
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

    def test_post_with_author_name(self, wt):
        author = AuthorFactory()

        url = url_for('books.BookList:post')
        title = fake.bs()
        res = wt.post_json(url,
            {
                'title': title,
                'author_first': author.first,
                'author_last': author.last,
            }
        )
        assert res.status_code == http.CREATED
        book = Book.get_latest()
        assert book.title == title
        latest_book_author = book.author
        assert author == latest_book_author

    def test_post_with_no_author(self, wt):
        url = url_for('books.BookList:post')
        title = fake.bs()
        res = wt.post_json(url,
            {
                'title': title
            }
        )
        assert res.status_code == http.CREATED
        book = Book.get_latest()
        assert book.title == title
        assert book.author is None

    def test_delete(self, wt):
        book = BookFactory()
        old_length = Book.query.count()
        url = url_for('books.BookDetail:delete', id=book.id)
        res = wt.delete(url)

        new_length = Book.query.count()
        assert new_length == old_length - 1


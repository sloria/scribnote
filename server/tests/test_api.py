# -*- coding: utf-8 -*-

import pytest
from flask import url_for
import httplib as http
from marshmallow.utils import isoformat

from server.app.books.models import Author, Book
from server.app.notes.models import Note
from .factories import AuthorFactory, BookFactory, NoteFactory
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
        assert data['created'] == isoformat(author.date_created)
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

@pytest.mark.usefixtures('db')
class TestNoteDetailResource:

    def test_get(self, wt):
        note = NoteFactory()
        url = url_for('notes.NoteDetail:get', id=note.id)
        res = wt.get(url)
        result = res.json['result']
        assert result['text'] == note.text

    def test_delete(self, wt):
        note = NoteFactory()
        old_count = Note.query.count()
        url = url_for('notes.NoteDetail:delete', id=note.id)
        res = wt.delete(url)
        new_count = Note.query.count()
        assert new_count == old_count - 1

    def test_put_update_text(self, wt):
        note = NoteFactory()
        url = url_for('notes.NoteDetail:put', id=note.id)
        new_text = fake.paragraph()
        res = wt.put_json(url, {'text': new_text})
        assert res.json['result']['text'] == new_text
        assert note.text == new_text

@pytest.mark.usefixtures('db')
class TestNoteListResource:

    def test_get(self, wt):
        note1, note2 = NoteFactory(), NoteFactory()
        url = url_for('notes.NoteList:get')
        res = wt.get(url)
        result = res.json['result']
        assert len(result) == Note.query.count()

    def test_post_creates_note(self, wt):
        book = BookFactory()
        url = url_for('notes.NoteList:post')
        old_count = Note.query.count()
        text = '\n'.join(fake.paragraphs(5))
        res = wt.post_json(url, {'text': text, 'book_id': book.id})
        assert res.status_code == http.CREATED
        new_count = Note.query.count()
        assert new_count == old_count + 1

        latest = Note.get_latest()
        assert latest.text == text

@pytest.mark.usefixtures('db')
class TestBookNoteNestedResource:

    @pytest.fixture
    def book(self, db):
        return BookFactory()

    @pytest.fixture
    def note(self, db, book):
        return NoteFactory(book=book)

    def test_url(self):
        assert url_for('books.notes', book_id=42) == '/api/books/42/notes/'

    def test_get_book_notes(self, wt, book):
        note1, note2 = NoteFactory(book=book), NoteFactory(book=book)
        url = url_for('books.notes', book_id=book.id)
        res = wt.get(url)
        result = res.json['result']
        assert len(result) == len(book.notes)

    def test_get_book_note(self, wt, book, note):
        url = url_for('books.note', book_id=book.id, note_id=note.id)
        res = wt.get(url)
        result = res.json['result']
        assert result['text'] == note.text
        assert 'book' in result

    def test_put_book_note(self, wt, book, note):
        url = url_for('books.note_edit', book_id=book.id, note_id=note.id)
        new_text = fake.paragraph()
        res = wt.put_json(url, {'text': new_text})
        assert res.status_code == 200
        assert note.text == new_text

    def test_delete_book_note(self, wt, book, note):
        old_length = Note.query.count()
        url = url_for('books.note_delete', book_id=book.id, note_id=note.id)
        res = wt.delete(url)
        new_length = Note.query.count()
        assert new_length == old_length - 1

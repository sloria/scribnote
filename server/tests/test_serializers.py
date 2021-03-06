# -*- coding: utf-8 -*-

import pytest
from marshmallow.utils import isoformat

from flask import url_for
from .factories import AuthorFactory, BookFactory, NoteFactory

from server.app.notes.serializers import NoteMarshal
from server.app.books.serializers import AuthorMarshal, BookMarshal

@pytest.mark.usefixtures('db')
class TestAuthorMarshal:

    def test_serialize_single(self):
        author = AuthorFactory()
        data = AuthorMarshal(author, strict=True).data
        assert data['first'] == author.first
        assert data['last'] == author.last
        assert data['created'] == isoformat(author.date_created)

    def test_serialize_single_links(self, app):
        author = AuthorFactory()
        data = AuthorMarshal(author, strict=True).data
        links = data['_links']
        assert links['self'] == url_for('books.AuthorDetail:get',
            id=author.id, _external=True)
        assert links['collection'] == url_for('books.AuthorList:get',
            _external=True)


@pytest.mark.usefixtures('db')
class TestBookMarshal:

    def test_serialize_single(self):
        book = BookFactory()
        data = BookMarshal(book, strict=True).data
        assert data['created'] == isoformat(book.date_created)
        assert 'author' in data

    def test_serialize_single_links(self):
        book = BookFactory()
        data = BookMarshal(book, strict=True).data
        links = data['_links']
        assert links['self'] == url_for('books.BookDetail:get',
            id=book.id, _external=True)
        assert links['collection'] == url_for('books.BookList:get',
            _external=True)


@pytest.mark.usefixtures('db')
class TestNoteMarshal:

    def test_serialize_single(self):
        note = NoteFactory()
        data = NoteMarshal(note, strict=True).data
        assert data['text'] == note.text
        assert 'created' in data

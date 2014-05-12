# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

from flask import url_for
import pytest

from server.app.users.models import User
from server.app.books.models import Book, Author, ReadingListItem
from server.app.notes.models import Note

from .factories import UserFactory, BookFactory, AuthorFactory, NoteFactory
from .utils import fake

@pytest.mark.usefixtures('db')
class TestUser:

    def test_get_by_id(self):
        user = User('foo', 'foo@bar.com')
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        user = User(email='foo@bar.com')
        user.save()
        assert bool(user.date_created)
        assert isinstance(user.date_created, dt.datetime)

    def test_password_is_nullable(self):
        user = User(email='foo@bar.com')
        user.save()
        assert user.password is None

    def test_factory(self):
        user = UserFactory(password="myprecious")
        assert bool(user.email)
        assert bool(user.date_created)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self):
        user = User.create(email="foo@bar.com",
                    password="foobarbaz123")
        assert user.check_password('foobarbaz123') is True
        assert user.check_password("barfoobaz") is False

    def test_full_name(self):
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

@pytest.mark.usefixtures('db')
class TestReadingLists:

    def test_user_can_add_to_reading_list(self):
        user = UserFactory()
        book = BookFactory()
        user.add_to_reading_list(book)
        user.save()

        assert book in user.reading_list.all()
        assert ReadingListItem.query.filter_by(user=user, book=book).count() == 1

    def test_user_has_read(self, db):
        user = UserFactory()
        book = BookFactory()
        user.add_to_reading_list(book)
        db.session.add(user)
        db.session.commit()
        assert user.has_read(book) is False

        rl = ReadingListItem.query.filter_by(user=user, book=book).first()
        rl.state = ReadingListItem.READ
        db.session.add(rl)
        db.session.commit()
        assert user.has_read(book) is True

    def test_mark_as_read(self, db):
        user, book = UserFactory(), BookFactory()
        user.add_to_reading_list(book)
        db.session.add(user)
        db.session.commit()
        user.mark_as_read(book)
        assert user.has_read(book) is True

    def test_mark_as_unread(self, db):
        user, book = UserFactory(), BookFactory()
        user.add_to_reading_list(book)
        user.save()
        rl = user.get_reading_list_item(book)
        rl.state = ReadingListItem.READ
        rl.save()
        assert user.has_read(book) is True
        user.mark_as_unread(book)
        user.save()
        assert user.has_read(book) is False



@pytest.mark.usefixtures('db')
class TestBook:

    def test_attributes(self):
        title = fake.sentence()
        book = Book.create(title=title)
        assert book.title == title
        assert hasattr(book, 'isbn')
        assert hasattr(book, 'author')
        assert hasattr(book, 'id')
        assert isinstance(book.id, int)
        assert isinstance(book.date_created, dt.datetime)

    def test_factory(self):
        book = BookFactory()
        assert book.title
        assert book.isbn
        assert book.author
        assert isinstance(book.author, Author)
        assert book.id


@pytest.mark.usefixtures('db')
class TestAuthor:

    def test_attributes(self):
        first, last = fake.first_name(), fake.last_name()
        author = Author.create(first=first, last=last)
        assert author.first == first
        assert author.last == last
        assert author.full_name == '{last}, {first}'.format(**locals())
        assert hasattr(author, 'id')
        assert isinstance(author.id, int)
        assert hasattr(author, 'books')

    def test_factory(self):
        author = AuthorFactory()
        assert author.first
        assert author.last
        assert author.id


@pytest.mark.usefixtures('db')
class TestNote:

    def test_attributes(self):
        book = BookFactory()
        text = fake.paragraph()
        note = Note.create(text=text, book=book)
        assert note.text == text
        assert isinstance(note.date_created, dt.datetime)
        assert note.book == book

    def test_note_delete_cascade(self):
        book = BookFactory()
        note = NoteFactory(book=book)
        assert Note.query.filter(Note.book == book).count() == 1
        book.delete(commit=True)
        assert Note.query.filter(Note.book == book).count() == 0

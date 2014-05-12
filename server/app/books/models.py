# -*- coding: utf-8 -*-

from ..meta.database import (
    Model,
    Col,
    db,
    SurrogatePK,
    ReferenceCol,
    relationship,
    DefaultDateTimeCol,
)


class Author(SurrogatePK, Model):
    __tablename__ = 'authors'

    first = Col(db.Unicode)
    last = Col(db.Unicode)
    date_created = DefaultDateTimeCol(nullable=False)

    _order_by = 'date_created'

    @property
    def full_name(self):
        return u'{self.last}, {self.first}'.format(self=self)

    def __init__(self, first, last, **kwargs):
        db.Model.__init__(self, first=first, last=last, **kwargs)

    def __repr__(self):
        return '<Author({self.full_name!r})>'.format(self=self)

class ReadingListItem(Model):
    """Association table that creates a many-to-many relationship between
    books and users.
    """
    __tablename__ = 'readinglistitems'

    book_id = ReferenceCol('books', primary_key=True)
    book = relationship('Book')
    user_id = ReferenceCol('users', primary_key=True)

    # "Read" states
    READ = 'read'
    UNREAD = 'unread'

    state = Col(db.Enum(READ, UNREAD), default=UNREAD)

    date_added = DefaultDateTimeCol()


class Book(SurrogatePK, Model):
    __tablename__ = 'books'

    _order_by = 'date_created'

    title = Col(db.String(255), unique=False, nullable=False)
    isbn = Col(db.String, nullable=True)
    date_created = DefaultDateTimeCol()

    # TODO: make many to many table
    author_id = ReferenceCol('authors', nullable=True)
    author = relationship('Author', backref='books')

    notes = relationship('Note', backref='book', cascade='all, delete, delete-orphan')

    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return '<Book(id={self.id!r}, title={self.title!r})>'.format(self=self)

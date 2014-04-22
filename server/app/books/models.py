# -*- coding: utf-8 -*-
from flask import url_for
from ..database import (
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
    date_created = DefaultDateTimeCol()

    _order_by = 'date_created'

    @property
    def full_name(self):
        return u'{self.last}, {self.first}'.format(self=self)

    def __init__(self, first, last, **kwargs):
        db.Model.__init__(self, first=first, last=last, **kwargs)

    def __repr__(self):
        return '<Author({self.full_name!r})>'.format(self=self)

    @property
    def url(self):
        return url_for('books.author', id=self.id)

    @property
    def absolute_url(self):
        return url_for('books.author', id=self.id, _external=True)

class Book(SurrogatePK, Model):
    __tablename__ = 'books'

    title = Col(db.String(255), unique=False, nullable=False)
    isbn = Col(db.String, nullable=True)
    date_created = DefaultDateTimeCol()

    # TODO: make many to many table
    author_id = ReferenceCol('authors', nullable=True)
    author = relationship('Author', backref='books')

    def __init__(self, title, **kwargs):
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        return '<Book(id={self.id!r}, title={self.title!r})>'.format(self=self)

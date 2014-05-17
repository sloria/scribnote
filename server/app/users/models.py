# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.login import UserMixin
from itsdangerous import (
    TimedJSONWebSignatureSerializer as TimedSerializer,
    SignatureExpired,
    BadSignature,
)

from ..extensions import bcrypt
from ..meta.database import (
    Column,
    db,
    Model,
    relationship,
    SurrogatePK,
    DefaultDateTimeCol
)
from ..books.models import ReadingListItem, Book


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    _order_by = 'date_created'
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    date_created = DefaultDateTimeCol()
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

    reading_list_items = relationship('ReadingListItem', backref='user')


    def __init__(self, email, password=None, **kwargs):
        db.Model.__init__(self, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def generate_token(self):
        auth_serializer = TimedSerializer(
            current_app.config['SECRET_KEY'],
            expires_in=current_app.config.get('AUTH_TOKEN_EXPIRE', 10 * 60)
        )
        return auth_serializer.dumps([self.id, self.password])

    @classmethod
    def get_from_token(cls, token):
        auth_serializer = TimedSerializer(
            current_app.config['SECRET_KEY']
        )
        try:
            data = auth_serializer.loads(token)
        except (BadSignature, SignatureExpired):
            return None
        return cls.get_by_id(data[0])

    @property
    def full_name(self):
        return "{0} {1}".format(self.first_name, self.last_name)

    def __repr__(self):
        return '<User({email!r})>'.format(email=self.email)

    def add_to_reading_list(self, book, state=ReadingListItem.UNREAD):
        reading_list_item = ReadingListItem(user=self, book=book, state=state)
        self.reading_list_items.append(reading_list_item)

    def remove_from_reading_list(self, book, commit=True):
        reading_list_item = self.get_reading_list_item(book)
        if not reading_list_item:
            raise ValueError('Book {0!r} is not in reading list.')
        reading_list_item.delete(commit=commit)

    @property
    def reading_list(self):
        return Book.query.join(ReadingListItem).filter_by(user=self)

    def get_reading_list_item(self, book):
        return ReadingListItem.query.filter_by(
            user=self, book=book
        ).first()

    def has_read(self, book):
        reading_list_item = self.get_reading_list_item(book)
        if not reading_list_item:
            return False
        else:
            return reading_list_item.state == ReadingListItem.READ

    def _set_item_state(self, book, state):
        """Helper for setting the state of a book on the user's reading list."""
        reading_list_item = self.get_reading_list_item(book)
        if not reading_list_item:
            raise ValueError('Cannot mark book that is not part of the user\'s '
                'reading list.')
        reading_list_item.state = state

    def mark_as_read(self, book):
        self._set_item_state(book, ReadingListItem.READ)

    def mark_as_unread(self, book):
        self._set_item_state(book, ReadingListItem.UNREAD)

    def toggle_read(self, book):
        if self.has_read(book):
            target_state = ReadingListItem.UNREAD
        else:
            target_state = ReadingListItem.READ
        self._set_item_state(book, target_state)

# -*- coding: utf-8 -*-
import datetime as dt

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
    ReferenceCol,
    relationship,
    SurrogatePK,
    DefaultDateTimeCol
)


class User(UserMixin, SurrogatePK, Model):

    __tablename__ = 'users'
    _order_by = 'date_created'
    email = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    date_created = Column(db.DateTime, default=dt.datetime.utcnow)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)

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
            expires_in=current_app.config.get('AUTH_TOKEN_EXPIRE', 5 * 60)
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
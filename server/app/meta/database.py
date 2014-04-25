# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
import datetime as dt
from sqlalchemy.orm import relationship

from ..extensions import db

# Alias common SQLAlchemy names
db = db
Column = Col = db.Column
relationship = relationship

class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD (create, read, update, delete)
    operations.
    """

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()

class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""
    __abstract__ = True

    _order_by = None

    @classmethod
    def get_first(cls):
        if cls._order_by is None:
            raise ValueError('Model does not define "_order_by"')
        order_by_attr = getattr(cls, cls._order_by)
        return cls.query.order_by(order_by_attr).first()

    @classmethod
    def get_latest(cls):
        if cls._order_by is None:
            raise ValueError('Model does not define "_order_by"')
        order_by_attr = getattr(cls, cls._order_by)
        return cls.query.order_by(order_by_attr.desc()).first()


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(object):
    """A mixin that adds a surrogate integer 'primary key' column named
    ``id`` to any declarative-mapped class.
    """
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id):
        if any(
            (isinstance(id, basestring) and id.isdigit(),
             isinstance(id, (int, float))),
        ):
            return cls.query.get(int(id))
        return None


def ReferenceCol(tablename, nullable=False, pk_name='id', **kwargs):
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id = ReferenceCol('category')
        category = relationship('Category', backref='categories')
    """
    return db.Column(
        db.ForeignKey("{0}.{1}".format(tablename, pk_name)),
        nullable=nullable, **kwargs)


def DefaultDateTimeCol(**kwargs):
    """Datetime column that defaults to utcnow."""
    return db.Column(
        db.DateTime,
        default=dt.datetime.utcnow
    )

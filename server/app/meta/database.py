# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related
utilities.
"""
import datetime as dt
from sqlalchemy.orm import relationship
from sqlalchemy.exc import OperationalError
from flask.ext.api.exceptions import NotFound
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

    @classmethod
    def get_or_create(cls, commit=True, **kwargs):
        query = cls.query.filter_by(**kwargs)
        if not query.count():
            instance = cls(**kwargs)
            instance.save(commit=commit)
            created = True
        else:
            if query.count() > 1:
                raise OperationalError('Multiple results found')
            instance = query.first()
            created = False
        return instance, created

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

    @classmethod
    def api_get_or_404(cls, id, error_msg=None):
        obj = cls.get_by_id(id)
        if obj is None:
            raise NotFound(detail=error_msg)
        return obj


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
        default=dt.datetime.utcnow,
        **kwargs
    )

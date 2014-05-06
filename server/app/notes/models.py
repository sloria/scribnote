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


class Note(SurrogatePK, Model):
    __tablename__ = 'notes'
    _order_by = 'date_created'

    text = Col(db.Unicode(5000))
    date_created = DefaultDateTimeCol(nullable=False)

    book_id = ReferenceCol('books')  # NOTE: relationship is defined in
                                     # Book model to allow for delete cascading

    def __init__(self, text, *args, **kwargs):
        self.text = text
        super(Note, self).__init__(**kwargs)

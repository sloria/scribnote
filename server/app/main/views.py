# -*- coding: utf-8 -*-
from flask import Blueprint, url_for, make_response


blueprint = Blueprint('main', __name__)


@blueprint.route('/')
def api_index():
    return {
        'message': 'Welcome to the Commonplace API. Follow the _links to get started.',
        '_links': {
            'books': url_for('books.BookList:get', _external=True),
            'authors': url_for('books.AuthorList:get', _external=True),
        }
    }

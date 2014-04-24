# -*- coding: utf-8 -*-
import mock
import pytest

from flask import url_for
from server.app.meta.api import Hyperlinks, URL, tpl, AbsoluteURL

@pytest.fixture
def mockauthor():
    author = mock.Mock()
    author.id = 123
    return author

@pytest.mark.parametrize('template', [
    '<<id>>',
    ' <<id>>',
    '<<id>> ',
    '<< id>>',
    '<<id  >>',
    '<< id >>',
])
def test_tpl(template):
    assert tpl(template) == 'id'
    assert tpl(template) == 'id'
    assert tpl(template) == 'id'

def test_bad_tpl():
    assert tpl('< <id>>') is None

def test_url_field(app, mockauthor):
    field = URL('books.author', id='<<id>>')
    result = field.output('url', mockauthor)
    assert result == url_for('books.author', id=mockauthor.id)

def test_hyperlinks_field(app, mockauthor):
    field = Hyperlinks({
        'self': URL('books.author', id='<<id>>'),
        'collection': URL('books.authors')
    })

    result = field.output('_links', mockauthor)
    assert result == {
        'self': url_for('books.author', id=mockauthor.id),
        'collection': url_for('books.authors')
    }

def test_hyperlinks_field_recurses(app, mockauthor):
    field = Hyperlinks({
        'self': {
            'href': URL('books.author', id='<<id>>'),
            'title': 'The author'
        },
        'collection': {
            'href': URL('books.authors'),
            'title': 'Authors list'
        }
    })
    result = field.output('_links', mockauthor)

    assert result == {
        'self': {'href': url_for('books.author', id=mockauthor.id),
                'title': 'The author'},
        'collection': {'href': url_for('books.authors'),
                        'title': 'Authors list'}
    }

def test_absolute_url(app, mockauthor):
    field = AbsoluteURL('books.authors')
    result = field.output('abs_url', mockauthor)
    assert result == url_for('books.authors', _external=True)

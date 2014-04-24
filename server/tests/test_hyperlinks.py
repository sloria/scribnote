# -*- coding: utf-8 -*-
import mock
import pytest

from flask import url_for
from server.app.meta.api import HyperlinksField, Link, tpl

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

def test_link_field(app, mockauthor):
    field = Link('books.author', id='<<id>>')
    result = field.output('url', mockauthor)
    assert result == url_for('books.author', id=mockauthor.id)

def test_hyperlinks_field(app, mockauthor):
    field = HyperlinksField({
        'self': Link('books.author', id='<<id>>'),
        'collection': Link('books.authors')
    })

    result = field.output('_links', mockauthor)
    assert result == {
        'self': url_for('books.author', id=mockauthor.id),
        'collection': url_for('books.authors')
    }

def test_hyperlinks_field_recurses(app, mockauthor):
    field = HyperlinksField({
        'self': {
            'href': Link('books.author', id='<<id>>'),
            'title': 'The author'
        },
        'collection': {
            'href': Link('books.authors'),
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

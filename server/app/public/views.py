# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify


blueprint = Blueprint('public', __name__)


@blueprint.route('/')
def index():
    return jsonify({
        'result': 'Nothing to see here'
    })

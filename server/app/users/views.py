# -*- coding: utf-8 -*-
import httplib as http
from flask import Blueprint, g, request, current_app, url_for
from webargs import Arg
from flask.ext.api.exceptions import NotFound

from ..meta.api import use_args, BadRequestError
from ..extensions import auth
from .models import User
from .serializers import UserSerializer

blueprint = Blueprint("users", __name__)
route = blueprint.route

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.get_from_token(username_or_token)

    if not user:
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

@route('/users/', methods=['GET'])
def users():
    return {
        'n_users': User.query.count(),
        '_links': {
            'register': url_for('users.register')
        }
    }

@route('/users/', methods=['POST'])
def register():
    email, password = request.data['email'], request.data['password']
    if User.query.filter_by(email=email).first() is not None:
        raise BadRequestError()
    user = User(email=email)
    user.set_password(password)
    user.save()
    return {
        'result': UserSerializer(user).data
    }, http.CREATED

@route('/users/<int:id>')
@auth.login_required
def user_detail(id):
    user = User.get_by_id(id)
    if not user:
        raise NotFound()
    return {
        'result': UserSerializer(user).data
    }

@route('/token/')
@auth.login_required
def get_token():
    token = g.user.generate_token()
    return {'result': token}

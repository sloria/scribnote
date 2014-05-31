# -*- coding: utf-8 -*-
import httplib as http
from flask import Blueprint, g, url_for, current_app
from webargs import Arg
from flask.ext.api.exceptions import NotFound, AuthenticationFailed
from flask.ext.classy import route
from flask.ext.jwt import jwt_required

from ..meta.api import (
    use_args,
    BadRequestError,
    ModelResource,
    register_class_views,
)
from ..extensions import jwt
from .models import User
from .serializers import UserSerializer

blueprint = Blueprint("users", __name__)
bp_route = blueprint.route

@jwt.response_handler
def make_token_response(token):
    return {
        'token': token
    }


@jwt.authentication_handler
def authentication_handler(username, password):
    user = User.query.filter_by(email=username).first()
    if user and user.check_password(password):
        return user
    return None


@jwt.error_handler
def auth_error_handler(error):
    return {
        'result': 'Authorization Required',
        'message': 'Authorization header was missing or invalid.'
    }, 401

@jwt.user_handler
def load_user(payload):
    return User.get_by_id(payload['user_id'])

@bp_route('/users/', methods=['GET'])
def users():
    return {
        'n_users': User.query.count(),
        '_links': {
            'register': url_for('users.register')
        }
    }

@bp_route('/users/', methods=['POST'])
@use_args({
    'email': Arg(required=True),
    'password': Arg(required=True)
}, targets=('data', 'json'))
def register(reqargs):
    email, password = reqargs['email'], reqargs['password']
    if User.query.filter_by(email=email).first() is not None:
        raise BadRequestError()
    user = User(email=email)
    user.set_password(password)
    user.save()
    return {
        'result': UserSerializer(user).data
    }, http.CREATED


class UserDetail(ModelResource):
    route_base = '/users/'
    MODEL = User
    SERIALIZER = UserSerializer

    decorators = [jwt_required()]

    def get(self, id):
        user = self.MODEL.api_get_or_404(id)
        res = {
            'result': self._serialize(user)
        }
        return res

    @route('/<id>/dashboard/')
    def dashboard(self, id):
        user = self.MODEL.api_get_or_404(id)
        return {
            'result': {
                'user': self._serialize(user),

            }
        }


register_class_views([UserDetail], blueprint)

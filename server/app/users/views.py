# -*- coding: utf-8 -*-
import httplib as http
from flask import Blueprint, g, url_for
from webargs import Arg
from flask.ext.api.exceptions import NotFound, AuthenticationFailed
from flask.ext.classy import route

from ..meta.api import (
    use_args,
    BadRequestError,
    ModelResource,
    register_class_views,
)
from ..extensions import auth
from .models import User
from .serializers import UserSerializer

blueprint = Blueprint("users", __name__)
bp_route = blueprint.route

@auth.verify_password
def verify_password(username_or_token, password):
    user = User.get_from_token(username_or_token)

    if not user:
        user = User.query.filter_by(email=username_or_token).first()
        if not user or not user.check_password(password):
            return False
    g.user = user
    return True

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

@bp_route('/users/<int:id>')
@auth.login_required
def user_detail(id):
    user = User.get_by_id(id)
    if not user:
        raise NotFound()
    return {
        'result': UserSerializer(user).data
    }

@bp_route('/token/')
@auth.login_required
def get_token():
    token = g.user.generate_token()
    return {'result': token}

@bp_route('/authenticate/', methods=['POST'])
@use_args({
    'username': Arg(required=True),
    'password': Arg(required=True)
}, targets=('data', 'json'))
def authenticate(reqargs):
    username, password = reqargs['username'], reqargs['password']
    user = User.query.filter_by(email=username).first()
    if user is None or not user.check_password(password):
        raise AuthenticationFailed()
    token = user.generate_token()
    return {
        'result': UserSerializer(user).data,
        'token': token,
    }

class UserDetail(ModelResource):
    route_base = '/users/'
    MODEL = User
    SERIALIZER = UserSerializer

    decorators = [auth.login_required]

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

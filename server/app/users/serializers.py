# -*- coding: utf-8 -*-

from ..extensions import ma


class UserSerializer(ma.Serializer):
    class Meta:
        additional = ('id', 'first_name', 'last_name')

    created = ma.DateTime(attribute='date_created')
    email = ma.Email()
    _links = ma.Hyperlinks({
        'self': ma.URL('users.user_detail', id='<id>')
    })

serialize_user = UserSerializer.factory(strict=True)

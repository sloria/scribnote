from flask import Blueprint
from flask.ext.restful import Api, Resource
from marshmallow import Serializer, fields

from ..utils import api_get_or_404
from .models import Author


blueprint = Blueprint('books', __name__)
api = Api(blueprint)

# Serializers

class AuthorMarshal(Serializer):
    created = fields.DateTime(attribute='date_created')

    class Meta:
        additional = ('first', 'last')

# Views

class AuthorResource(Resource):

    def get(self, id):
        """Return a single author."""
        author = api_get_or_404(Author, id, message="Author not found")
        return {
            'result': AuthorMarshal(author).data,
        }, 200


class AuthorListResource(Resource):

    def get(self):
        """Return a list of authors."""
        authors = Author.query.all()
        return {
            'result': AuthorMarshal(authors, many=True).data
        }, 200

api.add_resource(AuthorResource, '/authors/<int:id>', endpoint='author')
api.add_resource(AuthorListResource, '/authors/', endpoint='author_list')

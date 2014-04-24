# -*- coding: utf-8 -*-
from factory import (
    Sequence,
    PostGenerationMethodCall,
    LazyAttribute,
    SubFactory,
)
from factory.alchemy import SQLAlchemyModelFactory

from server.app.user.models import User
from server.app.books.models import Author, Book
from server.app.meta.database import db

from .utils import fake


class BaseFactory(SQLAlchemyModelFactory):
    FACTORY_SESSION = db.session

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""
        session = cls.FACTORY_SESSION
        obj = target_class(*args, **kwargs)
        session.add(obj)
        session.commit()
        return obj


class UserFactory(BaseFactory):
    FACTORY_FOR = User

    username = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True


class AuthorFactory(BaseFactory):
    FACTORY_FOR = Author

    first = LazyAttribute(lambda n: fake.first_name())
    last = LazyAttribute(lambda n: fake.last_name())


class BookFactory(BaseFactory):
    FACTORY_FOR = Book

    title = LazyAttribute(lambda n: fake.sentence(nb_words=4))
    isbn = LazyAttribute(lambda n: fake.md5())
    author = SubFactory(AuthorFactory)

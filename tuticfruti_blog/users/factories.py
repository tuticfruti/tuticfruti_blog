# -*- coding: utf-8 -*-
import factory
from . import models


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.User

    username = factory.Sequence(lambda n: 'user{:00}'.format(n))
    email = factory.LazyAttribute(lambda obj: '{}.example.com'.format(obj.username))
    password = '1234'

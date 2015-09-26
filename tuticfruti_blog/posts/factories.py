# -*- coding: utf-8 -*-
import datetime

import factory
import factory.fuzzy

from django.utils import timezone

from tuticfruti_blog.core import settings
from tuticfruti_blog.users import factories
from . import models


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Tag

    term = factory.Sequence(lambda n: 'term{}'.format(n))


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Post

    author = factory.SubFactory(factories.UserFactory)
    category_id = factory.fuzzy.FuzzyChoice([category_id for category_id, category_name in settings.CATEGORY_CHOICES])
    status_id = factory.fuzzy.FuzzyChoice([status_id for status_id, status_name in settings.POST_STATUS_CHOICES])
    title = factory.Sequence(lambda n: 'Post title {}'.format(n))
    content = factory.fuzzy.FuzzyChoice(settings.FUZZY_TEXTS)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.create(term=tag.term)


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Comment

    post = factory.SubFactory(PostFactory)
    author = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.LazyAttribute(lambda obj: '{}@example.com'.format(obj.author))
    status_id = factory.fuzzy.FuzzyChoice([status_id for status_id, status_name in settings.COMMENT_STATUS_CHOICES])
    content = factory.fuzzy.FuzzyChoice(settings.FUZZY_TEXTS)

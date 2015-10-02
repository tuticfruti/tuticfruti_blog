# -*- coding: utf-8 -*-
import factory
import factory.fuzzy

from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.users.factories import UserFactory
from . import models


class TagFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Tag

    term = factory.Sequence(lambda n: 'term{}'.format(n))


class CategoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Category

    name = factory.Sequence(lambda n: 'category{}'.format(n))
    order = factory.Sequence(lambda n: n)


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Post

    author = factory.SubFactory(UserFactory)
    status_id = factory.fuzzy.FuzzyChoice([status_id for status_id, status_name in models.Post.STATUS_CHOICES])
    title = factory.Sequence(lambda n: 'Post title {}'.format(n))
    content = factory.fuzzy.FuzzyChoice(data_fixtures.FUZZY_TEXTS)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.create(name=category.name)

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
    status_id = factory.fuzzy.FuzzyChoice(
        [status_id for status_id, status_name in models.Comment.STATUS_CHOICES])
    content = factory.fuzzy.FuzzyChoice(data_fixtures.FUZZY_TEXTS)
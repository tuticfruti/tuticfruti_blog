# -*- coding: utf-8 -*-
import factory
import factory.fuzzy

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


FUZZY_TEXTS = [
    'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Nam cursus. Morbi ut mi. Nullam enim leo, egestas id, condimentum at, <hr /> laoreet mattis, massa.',
    'Sed eleifend nonummy diam. Praesent mauris ante, elementum et, bibendum at, <hr /> posuere sit amet, nibh. Duis tincidunt lectus quis dui viverra vestibulum.',
    'Suspendisse vulputate aliquam dui. Nulla elementum dui ut augue. Aliquam vehicula mi at mauris. Maecenas placerat, nisl at consequat rhoncus, sem nunc gravida justo, quis eleifend arcu velit quis lacus. Morbi magna magna, <hr /> tincidunt a, mattis non, imperdiet vitae, tellus.',
    'Sed odio est, auctor ac, sollicitudin in, consequat vitae, orci. Fusce id felis. Vivamus sollicitudin metus eget eros.Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. <hr /> In posuere felis nec tortor. Pellentesque faucibus. Ut accumsan ultricies elit.',
    'Maecenas at justo id velit placerat molestie. Donec dictum lectus non odio. Cras a ante vitae enim iaculis aliquam. <hr /> Mauris nunc quam, venenatis nec, euismod sit amet, egestas placerat, est.',
    'Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Cras id elit. Integer quis urna. Ut ante enim, dapibus malesuada,fringilla eu, condimentum quis, tellus. Aenean porttitor eros vel dolor. <hr /> Donec convallis pede venenatis nibh. Duis quam. Nam eget lacus. Aliquam erat volutpat.']


class PostFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Post

    status_id = factory.fuzzy.FuzzyChoice([status_id for status_id, status_name in models.Post.STATUS_CHOICES])
    title = factory.Sequence(lambda n: 'Post title {}'.format(n))
    content = factory.fuzzy.FuzzyChoice(FUZZY_TEXTS)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.categories.add(category)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


class CommentFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Comment

    post = factory.SubFactory(PostFactory)
    author = factory.Sequence(lambda n: 'user{}'.format(n))
    email = factory.LazyAttribute(lambda obj: '{}@example.com'.format(obj.author))
    status_id = factory.fuzzy.FuzzyChoice(
        [status_id for status_id, status_name in models.Comment.STATUS_CHOICES])
    content = factory.fuzzy.FuzzyChoice(FUZZY_TEXTS)

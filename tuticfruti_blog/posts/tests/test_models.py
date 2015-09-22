# -*- coding: utf-8 -*-
from django.db import IntegrityError
from django.test import TestCase
from django.conf import settings
from django.contrib import admin

from tuticfruti_blog.users.factories import UserFactory
from .. import models
from .. import factories


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.post = factories.PostFactory(author=cls.user, title='Post title 0')
        cls.tag = factories.TagFactory(term='term')

    def test_app_belongs_to_local_apps(self):
        self.assertIn('tuticfruti_blog.posts', settings.LOCAL_APPS)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.post), 'Post title 0')

    def test_post_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/posts/{}/'.format(self.post.slug))

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Post))

    def test_post_generate_slug_from_title(self):
        self.assertEqual(self.post.slug, 'post-title-0')

    def test_cant_add_post_twice_with_same_slug(self):
        models.Post.objects.create(title='Post title must be unique', author=self.user)
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(title='Post title must be unique', author=self.user)

    def test_cant_add_post_without_author(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(title='Post author required')

    def test_saving_and_retrieving_items(self):
        post = factories.PostFactory(author=self.user, title='Post title 1')
        another_post = factories.PostFactory(author=self.user, title='Post title 2')
        saved_items = [
            models.Post.objects.get(title='Post title 1'),
            models.Post.objects.get(title='Post title 2')]

        self.assertEqual(models.Post.objects.count(), 3)
        self.assertEqual(saved_items[0].author, self.user)
        self.assertEqual(saved_items[0].title, post.title)
        self.assertEqual(saved_items[0].content, post.content)
        self.assertEqual(saved_items[1].author, self.user)
        self.assertEqual(saved_items[1].title, another_post.title)
        self.assertEqual(saved_items[1].content, another_post.content)


class TagModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):
        self.post = factories.PostFactory(author=self.user, title='Post title 0')

    def test_informal_string_representation(self):
        tag = models.Tag.objects.create(term='term')
        self.assertEqual(str(tag), 'term')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Tag))

    def test_saving_and_retrieving_items(self):
        tag1 = models.Tag.objects.create(term='tag1 term')
        tag2 = models.Tag.objects.create(term='tag2 term')
        saved_items = models.Tag.objects.all()
        self.assertEqual(saved_items.count(), 2)
        self.assertEqual(saved_items[0], tag1)
        self.assertEqual(saved_items[1], tag2)

    def test_cant_add_same_tag_twice(self):
        models.Tag.objects.create(term='tag term')
        with self.assertRaises(IntegrityError):
            models.Tag.objects.create(term='tag term')

    def test_adding_tags_to_post(self):
        tag = self.post.tags.create(term='term0')

        self.assertEqual(self.post.tags.count(), 1)
        self.assertEqual(tag.post_set.count(), 1)
        self.assertEqual(self.post.tags.get(term='term0'), tag)
        self.assertEqual(tag.post_set.get(title='Post title 0'), self.post)

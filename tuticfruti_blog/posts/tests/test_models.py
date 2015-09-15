# -*- coding: utf-8 -*-
from unittest import skip

from django.test import TestCase
from django.conf import settings
from django.contrib import admin

from tuticfruti_blog.users.models import User
from tuticfruti_blog.core.settings import PYTHON_CATEGORY
from ..models import Post


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='tuticfruti',
            email='tuticfruti@example.com',
            password='1234')

        cls.post = Post.objects.create(
            author=cls.user,
            title='Post title',
            content='<div></div>',
            category_id=PYTHON_CATEGORY)

    def test_post_in_local_apps(self):
        self.assertIn('tuticfruti_blog.posts', settings.LOCAL_APPS)

    def test_post_informal_string_representation(self):
        self.assertEqual(str(self.post), 'Post title')

    def test_post_absolute_url(self):
        self.assertEqual(self.post.get_absolute_url(), '/posts/{}/'.format(self.post.slug))

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(Post))

    def test_post_generate_slug_from_title(self):
        self.assertEqual(self.post.slug, 'post-title')

    def test_post_saving_and_retrieving_items(self):
        post2 = Post.objects.create(
            author=self.user,
            title='Post title 2',
            content='<div></div>',
            category_id=PYTHON_CATEGORY)

        self.assertEqual(Post.objects.all().count(), 2)

        saved_items = Post.objects.all()

        self.assertEqual(saved_items[0].author, self.user)
        self.assertEqual(saved_items[0].title, self.post.title)
        self.assertEqual(saved_items[0].content, self.post.content)
        self.assertEqual(saved_items[1].author, self.user)
        self.assertEqual(saved_items[1].title, post2.title)
        self.assertEqual(saved_items[1].content, post2.content)

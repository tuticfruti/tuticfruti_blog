# -*- coding: utf-8 -*-
import unittest

from django import test

from tuticfruti_blog.users.models import User
from .. import models
from .. import factories


class TestManagerBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user0')

        # Categories
        cls.enabled_category = factories.CategoryFactory(
            name='Category', is_enabled=True, order=1)
        cls.disabled_category = factories.CategoryFactory(
            name='Another category', is_enabled=False, order=2)

        # Posts
        cls.publised_post = factories.PostFactory(
            author=cls.user, status_id=models.Post.STATUS_PUBLISHED)
        cls.draf_post = factories.PostFactory(
            author=cls.user, status_id=models.Post.STATUS_DRAFT)

        # Comments
        cls.published_comment = factories.CommentFactory(
            post=cls.publised_post, status_id=models.Comment.STATUS_PUBLISHED)
        cls.draft_comment = factories.CommentFactory(
            post=cls.publised_post, status_id=models.Comment.STATUS_PENDING)


class TestPostManager(TestManagerBase):
    def test_all_published(self):
        queryset = models.Post.objects.all_published()

        self.assertEqual(queryset.count(), 1)

    def test_all_draft(self):
        queryset = models.Post.objects.all_draft()

        self.assertEqual(queryset.count(), 1)


class TestCommentManager(TestManagerBase):
    def test_all_published(self):
        queryset = models.Comment.objects.all_published()

        self.assertEqual(queryset.count(), 1)

    def test_all_pending(self):
        queryset = models.Comment.objects.all_pending()

        self.assertEqual(queryset.count(), 1)


class TestCategoryManager(TestManagerBase):
    def test_all_enabled(self):
        queryset = models.Category.objects.all_enabled()

        self.assertEqual(queryset.count(), 1)

# -*- coding: utf-8 -*-
import unittest

from django import test

from tuticfruti_blog.users.factories import UserFactory
from .. import models
from .. import factories


class TestPostManager(test.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.publised_post = factories.PostFactory(
            author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        self.draf_post = factories.PostFactory(
            author=self.user, status_id=models.Post.STATUS_DRAFT)

    def test_all_published(self):
        queryset = models.Post.objects.all_published()

        self.assertEqual(queryset.count(), 1)

    def test_all_draft(self):
        queryset = models.Post.objects.all_draft()

        self.assertEqual(queryset.count(), 1)


class TestCommentManager(test.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        self.published_comment = factories.CommentFactory(
            post=self.post, status_id=models.Comment.STATUS_PUBLISHED)
        self.draft_comment = factories.CommentFactory(
            post=self.post, status_id=models.Comment.STATUS_PENDING)

    def test_all_published(self):
        queryset = models.Comment.objects.all_published()

        self.assertEqual(queryset.count(), 1)

    def test_all_pending(self):
        queryset = models.Comment.objects.all_pending()

        self.assertEqual(queryset.count(), 1)


class TestCategoryManager(test.TestCase):
    def test_all_enabled(self):
        factories.CategoryFactory(name='Category', is_enabled=True, order=1)
        factories.CategoryFactory(name='Another category', is_enabled=False, order=2)
        queryset = models.Category.objects.all_enabled()

        self.assertEqual(queryset.count(), 1)

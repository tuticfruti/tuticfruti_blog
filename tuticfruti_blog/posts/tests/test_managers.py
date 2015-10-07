# -*- coding: utf-8 -*-
import unittest

from django import test

from tuticfruti_blog.core import data_fixtures
from .. import models


class TestManagerBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        data_fixtures.DataFixtures.load()


class TestPostManager(TestManagerBase):
    def test_all_published(self):
        posts_expected = models.Post.objects.filter(
            status_id=models.Post.STATUS_PUBLISHED)
        posts = models.Post.objects.all_published()

        self.assertEqual(posts.count(), posts_expected.count())

    def test_all_draft(self):
        posts_expected = models.Post.objects.filter(
            status_id=models.Post.STATUS_DRAFT)
        posts = models.Post.objects.all_draft()

        self.assertEqual(posts.count(), posts_expected.count())


class TestCommentManager(TestManagerBase):
    def test_all_published(self):
        comments_expected = models.Comment.objects.filter(
            status_id=models.Comment.STATUS_PUBLISHED)
        comments = models.Comment.objects.all_published()

        self.assertEqual(comments.count(), comments_expected.count())

    def test_all_pending(self):
        comments_expected = models.Comment.objects.filter(
            status_id=models.Comment.STATUS_PENDING)
        comments = models.Comment.objects.all_pending()

        self.assertEqual(comments.count(), comments_expected.count())


class TestCategoryManager(TestManagerBase):
    def test_all_enabled(self):
        categories_expected = models.Category.objects.filter(
            is_enabled=True)
        categories = models.Category.objects.all_enabled()

        self.assertEqual(categories.count(), categories_expected.count())

    def test_all_disabled(self):
        categories_expected = models.Category.objects.filter(
            is_enabled=False)
        categories = models.Category.objects.all_disabled()

        self.assertEqual(categories.count(), categories_expected.count())

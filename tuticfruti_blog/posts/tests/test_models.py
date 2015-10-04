# -*- coding: utf-8 -*-
import unittest

from django.db import IntegrityError
from django import test
from django.conf import settings
from django.contrib import admin
from django.utils import timezone

from tuticfruti_blog.users.models import User
from tuticfruti_blog.core import data_fixtures
from .. import models


class TestModelBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user0')
        cls.post = models.Post.objects.create(
            author=cls.user, title='Post title 0')
        cls.another_post = models.Post.objects.create(
            author=cls.user, title='Post title 1')


class TestPostModel(TestModelBase):
    def test_app_belongs_to_local_apps(self):
        self.assertIn('tuticfruti_blog.posts', settings.LOCAL_APPS)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.post), 'Post title 0')

    def test_post_absolute_url(self):
        self.assertEqual(
            self.post.get_absolute_url(), '/posts/{}/'.format(self.post.slug))

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Post))

    def test_post_generate_slug_from_title(self):
        self.assertEqual(self.post.slug, 'post-title-0')

    def test_saving_and_retrieving_items(self):
        saved_post = models.Post.objects.get(slug='post-title-0')

        self.assertEqual(saved_post.author, self.user)
        self.assertEqual(saved_post.title, self.post.title)
        self.assertEqual(saved_post.content, self.post.content)

    def test_author_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(title='Author must be not null')

    def test_author_field_must_exist(self):
        INEXINSTENT_ID = 999
        with self.assertRaises(ValueError):
            models.Post.objects.create(
                author=INEXINSTENT_ID, title='Author must exist')

    def test_title_field_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(author=self.user, title='Post title 0')

    def test_status_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(
                author=self.user,
                title='Status must be not null',
                status_id=None)

    def test_category_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(
                author=self.user,
                title='Category must be not null',
                status_id=None)

    def test_created_field_must_be_equal_to_today(self):
        self.assertEqual(self.post.created.date(), timezone.now().date())

    def test_modified_field_must_be_equal_to_today(self):
        self.assertEqual(self.post.modified.date(), timezone.now().date())

    def test_status_field_default_value(self):
        self.assertTrue(self.post.status_id, models.Post.STATUS_PUBLISHED)

    def test_default_ordering(self):
        queryset = models.Post.objects.all()

        self.assertEqual(queryset.first(), self.another_post)


class TestTagModel(TestModelBase):
    def setUp(self):
        self.tag = models.Tag.objects.create(term='term0')
        self.another_tag = models.Tag.objects.create(term='term1')
        self.post.tags.add(self.tag, self.another_tag)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.tag), 'term0')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Tag))

    def test_saving_and_retrieving_items(self):
        self.assertEqual(models.Tag.objects.get(term='term0'), self.tag)
        self.assertEqual(models.Tag.objects.get(term='term1'), self.another_tag)

    def test_term_field_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Tag.objects.create(term='term0')

    def test_term_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Tag.objects.create(term=None)

    def test_adding_tags_to_post(self):
        self.assertEqual(self.post.tags.count(), 2)

    def test_term_field_is_saved_in_lowercase(self):
        tag = models.Tag.objects.create(term='TeRm')
        self.assertEqual(tag.term, 'term')

    def test_default_ordering(self):
        tag = models.Tag.objects.create(term='_term')
        queryset = models.Tag.objects.all()

        self.assertEqual(queryset.first(), tag)


class TestCommentModel(TestModelBase):
    def setUp(self):
        self.comment = models.Comment.objects.create(
            post=self.post,
            author='user0',
            email='user0@example.com',
            content=data_fixtures.FUZZY_TEXTS[0])
        self.another_comment = models.Comment.objects.create(
            post=self.post,
            author='user1',
            email='user1@example.com',
            content=data_fixtures.FUZZY_TEXTS[1])
        self.post.comments.add(self.comment, self.another_comment)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.comment), data_fixtures.FUZZY_TEXTS[0])

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Comment))

    def test_saving_and_retrieving_items(self):
        self.assertEqual(
            models.Comment.objects.get(content=data_fixtures.FUZZY_TEXTS[0]),
            self.comment)
        self.assertEqual(
            models.Comment.objects.get(content=data_fixtures.FUZZY_TEXTS[1]),
            self.another_comment)

    def test_adding_comments_to_post(self):
        self.assertTrue(self.post.comments.count(), 2)

    def test_post_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_status_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                status_id=None,
                author='user0',
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_name_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_email_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_content_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com')

    def test_status_field_default_value(self):
        self.assertEqual(self.comment.status_id, models.Comment.STATUS_PENDING)

    def test_default_ordering(self):
        queryset = models.Comment.objects.all()

        self.assertEqual(queryset.first(), self.another_comment)


class TestCategoryModel(TestModelBase):
    def setUp(self):
        self.category = models.Category.objects.create(name='Category')
        self.another_category = models.Category.objects.create(
            name='Another category')
        self.post.categories.add(self.category, self.another_category)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.category), 'Category')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Category))

    def test_saving_and_retrieving_items(self):
        self.assertEqual(models.Category.objects.get(
            name='Category'), self.category)
        self.assertEqual(models.Category.objects.get(
            name='Another category'), self.another_category)

    def test_name_field_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Category.objects.create(name='Category')

    def test_name_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Category.objects.create(name=None)

    def test_order_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Category.objects.create(order=None)

    def test_is_enabled_field_default_value(self):
        self.assertTrue(self.category.is_enabled)

    def test_default_ordering(self):
        self.category.order = 2
        self.category.save()
        self.another_category.order = 1
        self.another_category.save()
        queryset = models.Category.objects.all()

        self.assertEqual(queryset.first(), self.another_category)

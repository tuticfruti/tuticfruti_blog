# -*- coding: utf-8 -*-
import unittest

from django.db import IntegrityError
from django import test
from django.conf import settings as settings
from django.contrib import admin
from django.utils import timezone

from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.core import data_fixtures
from .. import models
from .. import factories


class PostModelTest(test.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(author=self.user, title='Post title 0')
        self.another_post = factories.PostFactory(author=self.user, title='Post title 1')

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

    def test_saving_and_retrieving_items(self):
        category = factories.CategoryFactory(name='Category')
        tag = factories.TagFactory(term='term')
        post = factories.PostFactory(author=self.user, title='Post')
        post.categories.add(category)
        post.tags.add(tag)
        another_post = factories.PostFactory(author=self.user, title='Another post')
        another_post.categories.add(category)
        another_post.tags.add(tag)
        saved_items = [
            models.Post.objects.get(title='Post'),
            models.Post.objects.get(title='Another post')]

        self.assertEqual(saved_items[0].author, self.user)
        self.assertEqual(saved_items[0].title, post.title)
        self.assertEqual(saved_items[0].content, post.content)
        self.assertEqual(saved_items[0].categories.get(name='Category'), category)
        self.assertEqual(saved_items[1].author, self.user)
        self.assertEqual(saved_items[1].title, another_post.title)
        self.assertEqual(saved_items[1].content, another_post.content)
        self.assertEqual(saved_items[1].categories.get(name='Category'), category)

    def test_author_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(title='Author must exist')

    def test_author_must_exist(self):
        user = UserFactory.build()
        with self.assertRaises(ValueError):
            models.Post.objects.create(author=user, title='Author must exist')

    def test_title_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(author=self.user, title='Post title 0')

    def test_status_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(author=self.user, title='Status must be not null', status_id=None)

    def test_integrity_category_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(author=self.user, title='Category must be not null', status_id=None)

    def test_created_datetime_must_be_equal_to_today(self):
        self.assertEqual(self.post.created.date(), timezone.now().date())

    def test_modified_datetime_must_be_equal_to_today(self):
        self.assertEqual(self.post.modified.date(), timezone.now().date())

    def test_status_default_value(self):
        self.assertTrue(self.post.status_id, models.Post.STATUS_PUBLISHED)


class TagModelTest(test.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(author=self.user, title='Post title 0')
        self.tag = models.Tag.objects.create(term='term0')
        self.another_tag = models.Tag.objects.create(term='term1')

    def test_informal_string_representation(self):
        self.assertEqual(str(self.tag), 'term0')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Tag))

    def test_saving_and_retrieving_items(self):
        saved_items = [
            models.Tag.objects.get(term='term0'),
            models.Tag.objects.get(term='term1')]
        self.assertEqual(saved_items[0], self.tag)
        self.assertEqual(saved_items[1], self.another_tag)

    def test_tag_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            models.Tag.objects.create(term='term0')

    def test_tag_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Tag.objects.create(term=None)

    def test_adding_tags_to_post(self):
        self.post.tags.add(self.tag)
        self.post.tags.add(self.another_tag)

        self.assertEqual(self.post.tags.count(), 2)

    def test_term_tag_is_saved_in_lowercase(self):
        tag = models.Tag.objects.create(term='TeRm')
        self.assertEqual(tag.term, 'term')

class CommentModelTest(test.TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(author=self.user, title='Post title')
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

    def test_informal_string_representation(self):
        self.assertEqual(str(self.comment), data_fixtures.FUZZY_TEXTS[0])

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Comment))

    def test_saving_and_retrieving_items(self):
        saved_items = [
            models.Comment.objects.get(content=data_fixtures.FUZZY_TEXTS[0]),
            models.Comment.objects.get(content=data_fixtures.FUZZY_TEXTS[1])]
        self.assertEqual(saved_items[0], self.comment)
        self.assertEqual(saved_items[1], self.another_comment)

    def test_adding_comments_to_post(self):
        post = factories.PostFactory(title='Adding comments to post')
        post.comments.add(self.comment)
        post.comments.add(self.another_comment)

        self.assertTrue(post.comments.count(), 2)

    def test_post_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_status_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                status_id=None,
                author='user0',
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_name_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_email_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                content=data_fixtures.FUZZY_TEXTS[0])

    def test_content_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com')

    def test_status_default_value(self):
        self.assertEqual(self.comment.status_id, models.Comment.STATUS_PENDING)


class CategoryModelTest(test.TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_informal_string_representation(self):
        category = models.Category.objects.create(name='Python category')
        self.assertEqual(str(category), 'Python category')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Category))

    def test_saving_and_retrieving_items(self):
        category = models.Category.objects.create(name='Category')
        another_category = models.Category.objects.create(name='Another category')
        saved_items = [
            models.Category.objects.get(name='Category'),
            models.Category.objects.get(name='Another category')]

        self.assertEqual(saved_items[0], category)
        self.assertEqual(saved_items[1], another_category)


    def test_name_must_be_unique(self):
        category = models.Category.objects.create(name='Python category')
        with self.assertRaises(IntegrityError):
            another_category = models.Category.objects.create(name='Python category')

    def test_name_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            category = models.Category.objects.create(name=None)

    def test_order_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            category = models.Category.objects.create(order=None)

    def test_is_active_default_value(self):
        category = models.Category.objects.create(name='Python category')
        self.assertTrue(category.is_active)

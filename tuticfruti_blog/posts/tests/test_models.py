# -*- coding: utf-8 -*-
import unittest

from django.db import IntegrityError
from django import test
from django.conf import settings
from django.contrib import admin
from django.utils import timezone

from tuticfruti_blog.users.models import User
from .. import models
from .. import factories


class TestModelBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):

        # Users
        cls.user = User.objects.create_user(username='user0')

        # Posts
        cls.published_posts = models.Post.objects \
            .filter(status_id=models.Post.STATUS_PUBLISHED)
        cls.published_post = models.Post.objects.create(
            author=cls.user, title='Post title 0')
        cls.another_post = models.Post.objects.create(
            author=cls.user, title='Post title 1')

        # Tags
        cls.tags = models.Tag.objects.all()
        cls.tag = models.Tag.objects.create(term='term0')
        cls.another_tag = models.Tag.objects.create(term='term1')
        cls.published_post.tags.add(cls.tag, cls.another_tag)

        # Comments
        cls.comment = models.Comment.objects.create(
            post=cls.published_post,
            author='author0',
            email='author0@example.com',
            content=factories.FUZZY_TEXTS[0])
        cls.another_comment = models.Comment.objects.create(
            post=cls.published_post,
            author='author1',
            email='author1@example.com',
            content=factories.FUZZY_TEXTS[1])


class TestPostModel(TestModelBase):
    def test_app_belongs_to_local_apps(self):
        self.assertIn('tuticfruti_blog.posts', settings.LOCAL_APPS)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.published_post), 'Post title 0')

    def test_post_absolute_url(self):
        self.assertEqual(
            self.published_post.get_absolute_url(),
            '/posts/{}/'.format(self.published_post.slug))

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Post))

    def test_post_generate_slug_from_title(self):
        self.assertEqual(self.published_post.slug, 'post-title-0')

    def test_saving_and_retrieving_items(self):
        saved_post = models.Post.objects.get(slug='post-title-0')

        self.assertEqual(saved_post.author, self.user)
        self.assertEqual(saved_post.title, self.published_post.title)
        self.assertEqual(saved_post.content, self.published_post.content)

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

    def test_created_field_must_be_equal_to_today_date(self):
        self.assertEqual(
            self.published_post.created.date(), timezone.now().date())

    def test_modified_field_must_be_equal_to_today_date(self):
        self.assertEqual(
            self.published_post.modified.date(), timezone.now().date())

    def test_status_field_default_value(self):
        self.assertTrue(self.published_post.status_id, models.Post.STATUS_PUBLISHED)

    def test_posts_are_sorted_by_created_field(self):
        post = models.Post.objects.create(
            title='Test posts are sorted by created_field',
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED)

        self.assertEqual(post, self.published_posts.first())


class TestTagModel(TestModelBase):
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
        self.assertEqual(self.published_post.tags.count(), 2)

    def test_term_field_is_saved_in_lowercase(self):
        tag = models.Tag.objects.create(term='TeRm')
        self.assertEqual(tag.term, 'term')

    def test_default_ordering(self):
        tag = models.Tag.objects.create(term='_term')

        self.assertEqual(self.tags.first(), tag)


class TestCommentModel(TestModelBase):
    def test_informal_string_representation(self):
        self.assertEqual(str(self.comment), factories.FUZZY_TEXTS[0])

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Comment))

    def test_saving_and_retrieving_items(self):
        self.assertEqual(
            models.Comment.objects.get(content=factories.FUZZY_TEXTS[0]),
            self.comment)
        self.assertEqual(
            models.Comment.objects.get(content=factories.FUZZY_TEXTS[1]),
            self.another_comment)

    def test_adding_comments_to_post(self):
        self.assertTrue(self.published_post.comments.count(), 2)

    def test_post_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com',
                content=factories.FUZZY_TEXTS[0])

    def test_status_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                status_id=None,
                author='user0',
                email='user0@example.com',
                content=factories.FUZZY_TEXTS[0])

    def test_name_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                email='user0@example.com',
                content=factories.FUZZY_TEXTS[0])

    def test_email_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                content=factories.FUZZY_TEXTS[0])

    def test_content_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Comment.objects.create(
                author='user0',
                email='user0@example.com')

    def test_status_field_default_value(self):
        self.assertEqual(self.comment.status_id, models.Comment.STATUS_PENDING)

    def test_comment_are_sorted_by_created_field(self):
        comment = models.Comment.objects.create(
            post=self.published_post,
            author='anonymous',
            email='anonymous@example.com',
            content='Content ...')

        self.assertEqual(comment, self.published_post.comments.first())

    def test_created_field_must_be_equal_to_today_date(self):
        self.assertEqual(self.comment.created.date(), timezone.now().date())

    def test_modified_field_must_be_equal_to_today_date(self):
        self.assertEqual(self.comment.modified.date(), timezone.now().date())


class TestCategoryModel(TestModelBase):
    def setUp(self):
        self.category = models.Category.objects.create(
            name='Category', order=2)
        self.another_category = models.Category.objects.create(
            name='Another category', order=1)
        self.published_post.categories.add(self.category, self.another_category)

    def test_informal_string_representation(self):
        self.assertEqual(str(self.category), 'Category')

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Category))

    def test_saving_and_retrieving_items(self):
        self.assertEqual(models.Category.objects.get(
            slug='category'), self.category)
        self.assertEqual(models.Category.objects.get(
            slug='another-category'), self.another_category)

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
        queryset = models.Category.objects.all()

        self.assertEqual(queryset.first(), self.another_category)

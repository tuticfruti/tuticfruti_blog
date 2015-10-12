# -*- coding: utf-8 -*-
import unittest

from django.core.urlresolvers import reverse
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
            author=cls.user,
            title='Post title 0',
            content=factories.FUZZY_TEXTS[0])
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
        str_expected = 'Post title 0'
        str_ = str(self.published_post)

        self.assertEqual(str_, str_expected)

    def test_post_absolute_url(self):
        url_path_expected = reverse(
            'posts:detail', kwargs=dict(slug=self.published_post.slug))
        url_path = self.published_post.get_absolute_url()

        self.assertEqual(url_path, url_path_expected)

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Post))

    def test_post_generate_slug_from_title(self):
        slug_expected = 'post-title-0'
        slug = self.published_post.slug

        self.assertEqual(slug, slug_expected)

    def test_saving_and_retrieving_items(self):
        post_expected = self.published_post
        saved_post = models.Post.objects.get(slug='post-title-0')

        self.assertEqual(saved_post.categories, post_expected.categories)
        self.assertEqual(saved_post.author, self.user)
        self.assertEqual(saved_post.title, post_expected.title)
        self.assertEqual(saved_post.slug, post_expected.slug)
        self.assertEqual(saved_post.content, post_expected.content)
        self.assertEqual(saved_post.status_id, post_expected.status_id)
        self.assertEqual(saved_post.tags, post_expected.tags)
        self.assertEqual(saved_post.created, post_expected.created)
        self.assertEqual(saved_post.modified, post_expected.modified)

    def test_author_field_must_be_not_null(self):
        with self.assertRaises(IntegrityError):
            models.Post.objects.create(title='Author must be not null')

    def test_author_field_must_exist(self):
        post = models.Post(
            author=User(username='user0'), title='Author must exist')

        with self.assertRaises(ValueError):
            post.save()

    def test_title_field_must_be_unique(self):
        post = models.Post(author=self.user, title='Post title 0')

        with self.assertRaises(IntegrityError):
            post.save()

    def test_status_field_must_be_not_null(self):
        post = models.Post(
            author=self.user, title='Status must be not null', status_id=None)

        with self.assertRaises(IntegrityError):
            post.save()

    def test_category_field_must_be_not_null(self):
        post = models.Post(
            author=self.user, title='Category must be not null', status_id=None)

        with self.assertRaises(IntegrityError):
            post.save()

    def test_created_field_must_be_equal_to_today_date(self):
        date_expected = timezone.now().date()
        date = self.published_post.created.date()

        self.assertEqual(date, date_expected)

    def test_modified_field_must_be_equal_to_today_date(self):
        date_expected = timezone.now().date()
        date = self.published_post.modified.date()

        self.assertEqual(date, date_expected)

    def test_status_field_default_value(self):
        status_espected = models.Post.STATUS_PUBLISHED
        status = self.published_post.status_id

        self.assertTrue(status, status_espected)

    def test_posts_are_sorted_by_created_field(self):
        post = models.Post.objects.create(
            title='Test posts are sorted by created_field',
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED)
        post_expected = self.published_posts.first()

        self.assertEqual(post, post_expected)


class TestTagModel(TestModelBase):
    def test_informal_string_representation(self):
        str_expected = 'term0'
        str_ = str(self.tag)

        self.assertEqual(str_, str_expected)

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Tag))

    def test_saving_and_retrieving_items(self):
        tags_expected = ['term0', 'term1']
        tags = [self.tag, self.another_tag]

        for i in range(len(tags)):
            self.assertEqual(tags[i].term, tags_expected[i])

    def test_term_field_must_be_unique(self):
        tag = models.Tag(term='term0')

        with self.assertRaises(IntegrityError):
            tag.save()

    def test_term_field_must_be_not_null(self):
        tag = models.Tag(term=None)

        with self.assertRaises(IntegrityError):
            tag.save()

    def test_adding_tags_to_post(self):
        num_tags_expected = 2
        num_tags = self.published_post.tags.count()

        self.assertEqual(num_tags, num_tags_expected)

    def test_default_ordering(self):
        tag_expected = models.Tag.objects.create(term='_term')
        tag = self.tags.first()

        self.assertEqual(tag, tag_expected)


class TestCommentModel(TestModelBase):
    def test_informal_string_representation(self):
        str_expected = factories.FUZZY_TEXTS[0]
        str_ = str(self.comment)

        self.assertEqual(str_, str_expected)

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Comment))

    def test_saving_and_retrieving_items(self):
        comments_expected = [self.comment, self.another_comment]
        comments = [
            models.Comment.objects.get(content=factories.FUZZY_TEXTS[0]),
            models.Comment.objects.get(content=factories.FUZZY_TEXTS[1])]

        for i in range(len(comments)):
            self.assertEqual(comments[i], comments_expected[i])

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
        status_expected = models.Comment.STATUS_PENDING
        status = self.comment.status_id

        self.assertEqual(status, status_expected)

    def test_comment_are_sorted_by_created_field(self):
        comment_expected = models.Comment.objects.create(
            post=self.published_post,
            author='anonymous',
            email='anonymous@example.com',
            content='Content ...')
        comment = self.published_post.comments.first()

        self.assertEqual(comment, comment_expected)

    def test_created_field_must_be_equal_to_today_date(self):
        date_expected = timezone.now().date()
        date = self.comment.created.date()

        self.assertEqual(date, date_expected)

    def test_modified_field_must_be_equal_to_today_date(self):
        date_expected = timezone.now().date()
        date = self.comment.modified.date()

        self.assertEqual(date, date_expected)


class TestCategoryModel(TestModelBase):
    def setUp(self):
        self.category = models.Category.objects.create(
            name='Category', order=2)
        self.another_category = models.Category.objects.create(
            name='Another category', order=1)
        self.published_post.categories.add(self.category, self.another_category)

    def test_informal_string_representation(self):
        category_expected = 'Category'
        category = str(self.category)

        self.assertEqual(category, category_expected)

    def test_post_registered_in_admin_backend(self):
        self.assertTrue(admin.site.is_registered(models.Category))

    def test_saving_and_retrieving_items(self):
        slugs_expected = ['category', 'another-category']
        slugs = [
            models.Category.objects.get(slug='category'),
            models.Category.objects.get(slug='another-category')]

        for i in range(len(slugs)):
            self.assertEqual(slugs[i].slug, slugs_expected[i])

    def test_name_field_must_be_unique(self):
        category = models.Category(name='Category')

        with self.assertRaises(IntegrityError):
            category.save()

    def test_name_field_must_be_not_null(self):
        category = models.Category(name=None)

        with self.assertRaises(IntegrityError):
            category.save()

    def test_order_field_must_be_not_null(self):
        category = models.Category(order=None)

        with self.assertRaises(IntegrityError):
            category.save()

    def test_is_enabled_field_default_value(self):
        self.assertTrue(self.category.is_enabled)

    def test_sort_by_order_field_asc(self):
        category_expected = self.another_category
        category = models.Category.objects.first()

        self.assertEqual(category, category_expected)

    def test_generate_slug_from_name_field(self):
        slug_expected = 'name-with-multiple-words'
        slug = models.Category.objects.create(name='Name with multiple words').slug

        self.assertEqual(slug, slug_expected)

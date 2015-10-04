# -*- coding: utf-8 -*-
import unittest
import datetime

from django.core.urlresolvers import reverse
from django import test
from django.utils import timezone

from .. import models
from .. import views
from .. import factories
from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.users.models import User


class TestViewBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        # Users
        cls.user = User.objects.create_user(username='user0')

        # Categories
        cls.miscellaneous_category = factories.CategoryFactory(
            name='Miscellaneous', order=3)
        cls.django_category = factories.CategoryFactory(
            name='Django', order=2)
        cls.python_category = factories.CategoryFactory(
            name='Python', order=1)
        cls.disabled_category = factories.CategoryFactory(
            name='Disabled category', is_enabled=False, order=4)

        # Tags
        cls.python_tag = factories.TagFactory(term='python')
        cls.django_tag = factories.TagFactory(term='django')
        cls.miscellaneous_tag = factories.TagFactory(term='miscellaneous')

        # Posts
        cls.post = factories.PostFactory(
            title='Post title',
            author=cls.user,
            status_id=models.Post.STATUS_PUBLISHED,
            content=data_fixtures.FUZZY_TEXTS[5])
        cls.post.categories.add(
            cls.python_category,
            cls.django_category,
            cls.miscellaneous_category)
        cls.post.tags.add(
            cls.python_tag, cls.django_tag, cls.miscellaneous_tag)
        cls.draft_post = factories.PostFactory(
            author=cls.user,
            title='Draft post',
            status_id=models.Post.STATUS_DRAFT)
        cls.python_post = factories.PostFactory(
            title='Python post',
            author=cls.user,
            status_id=models.Post.STATUS_PUBLISHED)
        cls.python_post.categories.add(cls.python_category)
        cls.python_post.tags.add(cls.python_tag)
        cls.django_post = factories.PostFactory(
            title='Django post',
            author=cls.user,
            status_id=models.Post.STATUS_PUBLISHED)
        cls.django_post.categories.add(cls.django_category)
        cls.django_post.tags.add(cls.django_tag)
        cls.miscellaneous_post = factories.PostFactory(
            title='Miscellaneous post',
            author=cls.user,
            status_id=models.Post.STATUS_PUBLISHED)
        cls.miscellaneous_post.categories.add(cls.miscellaneous_category)
        cls.miscellaneous_post.tags.add(cls.miscellaneous_tag)

        # Comments
        cls.published_comment = factories.CommentFactory(
            post=cls.post,
            status_id=models.Comment.STATUS_PUBLISHED)
        cls.pending_comment = factories.CommentFactory(
            post=cls.post,
            status_id=models.Comment.STATUS_PENDING)


class TestPostListView(TestViewBase):
    def setUp(self):
        self.res = self.client.get(reverse('home'))

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res.resolver_match.func.__name__,
            views.PostListView.as_view().__name__)

    def test_posts_variable_is_available_in_context_data(self):
        self.assertIn('posts', self.res.context_data)

    def test_categories_variagle_is_available_in_context_data(self):
        self.assertIn('categories', self.res.context_data)

    def test_content_limit_variable_is_available_in_context_data(self):
        self.assertIn('post_text_content_limit', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_only_public_posts_are_displayed(self):
        self.assertNotIn(self.draft_post, self.res.context_data.get('posts'))

    def test_all_categories_are_sorted(self):
        sorted_categories_expected = [
            self.python_category,
            self.django_category,
            self.miscellaneous_category]
        sorted_categories = self.res.context_data.get('categories').all()

        i = 0
        for i in range(len(sorted_categories)):
            self.assertEqual(
                sorted_categories[i], sorted_categories_expected[i])

    def test_categories_displayed_are_enabled(self):
        self.assertNotIn(
            self.disabled_category,
            self.res.context_data.get('categories'))

    def test_all_post_categories_are_enabled(self):
        post = self.res.context_data.get('posts').last()
        post_categories = post.categories.all()
        self.assertNotIn(self.disabled_category, post_categories)

    def test_all_post_categories_are_sorted(self):
        post = self.res.context_data.get('posts').last()
        post_categories = post.categories.all()
        sorted_categories = [
            self.python_category,
            self.django_category,
            self.miscellaneous_category]

        self.assertSequenceEqual(
            post_categories,
            sorted_categories)

    def test_all_post_tags_are_sorted_by_alphabetical_order(self):
        tag = factories.TagFactory(term='_term')
        self.post.tags.add(tag)
        res = self.client.get(reverse('home'))
        post = res.context_data.get('posts').last()

        self.assertEqual(post.tags.first(), tag)

    def test_all_post_comments_are_published(self):
        post_comments = self.res.context_data.get('posts').last()

        self.assertEqual(post_comments.comments.count(), 1)


class TestPostListByCategoryView(TestViewBase):
    def setUp(self):
        self.res = self.client.get(reverse(
            'posts:list_by_category',
            kwargs=dict(slug=self.python_category.slug)))

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res.resolver_match.func.__name__,
            views.PostListByCategoryView.as_view().__name__)

    def test_current_category_variable_is_available_in_context_data(self):
        self.assertIn('current_category', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_filter_posts_by_python_category(self):
        posts = [self.python_post, self.post]
        self.assertEqual(self.res.context_data.get('posts').count(), 2)
        self.assertSequenceEqual(
            self.res.context_data.get('posts'),
            posts)


class TestPostListSearchView(TestViewBase):
    def setUp(self):
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms='python'))

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res.resolver_match.func.__name__,
            views.PostListSearchView.as_view().__name__)

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_search_terms_variable_is_available_in_context_data(self):
        self.assertIn('search_terms', self.res.context_data)

    def test_search_is_case_insensitive(self):
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms=self.python_tag.term.upper()))

        self.assertEqual(self.res.context_data.get('posts').count(), 2)

    def test_result_has_no_repeated(self):
        search_terms = '{} {}'.format(
            self.python_tag.term,
            self.python_tag.term)
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms=search_terms))

        self.assertEqual(self.res.context_data.get('posts').count(), 2)

    def test_restrict_result_by_category(self):
        search_terms = '{} {} {}'.format(
            self.python_tag.term,
            self.django_tag.term,
            self.miscellaneous_tag.term)
        self.res = self.client.get(
            reverse(
                'posts:search_by_category',
                kwargs=dict(slug=self.python_category.slug)),
            dict(search_terms=search_terms))

        self.assertEqual(self.res.context_data.get('posts').count(), 2)


class TestPostDetailView(TestViewBase):
    def setUp(self):
        self.res = self.client.get(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)))

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res.resolver_match.func.__name__,
            views.PostDetailView.as_view().__name__)

    def test_post_variable_is_available_in_context_data(self):
        self.assertIn('post', self.res.context_data)

    def test_form_variable_is_available_in_context_data(self):
        self.assertIn('form', self.res.context_data)

    def test_categories_variable_is_available_in_context_data(self):
        self.assertIn('categories', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/detail.html', self.res.template_name)

    def test_send_a_valid_form_comment(self):
        res = self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)),
            dict(
                author='user0',
                email='user0@example.com',
                content=data_fixtures.FUZZY_TEXTS[0]),
            follow=True)

        self.assertEqual(self.post.comments.count(), 3)
        self.assertIn(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)),
            res.redirect_chain[0][0])

    def test_send_an_invalid_form_comment(self):
        self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)),
            dict(
                author=None,
                email=None,
                content=None))

        self.assertEqual(self.post.comments.count(), 2)

    def test_comments_are_sorted_by_created_field(self):
        # New published post
        post = factories.PostFactory(
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED)

        # New published comment created at January 2015
        comment = factories.CommentFactory(
            post=post,
            status_id=models.Comment.STATUS_PUBLISHED)
        comment.created = datetime.datetime(
            2015, 1, 1, tzinfo=timezone.get_current_timezone())
        comment.save()

        # New published comment created at February 2015
        another_comment = factories.CommentFactory(
            post=post,
            status_id=models.Comment.STATUS_PUBLISHED)
        another_comment.created = datetime.datetime(
            2015, 2, 1, tzinfo=timezone.get_current_timezone())
        another_comment.save()

        # Request post details
        res = self.client.get(
            reverse('posts:detail', kwargs=dict(slug=post.slug)))

        self.assertEqual(
            res.context_data.get('post').comments.first(), another_comment)
        self.assertEqual(
            res.context_data.get('post').comments.last(), comment)

    def test_all_post_tags_are_sorted_by_alphabetical_order(self):
        sorted_tags_expected = [
            self.django_tag, self.miscellaneous_tag, self.python_tag]
        sorted_tags = self.res.context_data.get('post').tags.all()

        i = 0
        for i in range(len(sorted_tags)):
            self.assertEqual(sorted_tags[i], sorted_tags_expected[i])

    def test_all_categories_are_sorted(self):
        sorted_categories_expected = [
            self.python_category,
            self.django_category,
            self.miscellaneous_category]
        sorted_categories = self.res.context_data.get('post').categories.all()

        i = 0
        for i in range(len(sorted_categories)):
            self.assertEqual(
                sorted_categories[i], sorted_categories_expected[i])

    def test_categories_displayed_are_enabled(self):
        self.assertNotIn(
            self.disabled_category,
            self.res.context_data['post'].categories.all())

    def test_only_published_comments_are_counted(self):
        self.assertEqual(self.res.context_data.get('post').comments.count(), 1)

    def test_only_published_comments_are_displayed(self):
        self.assertNotIn(
            self.pending_comment,
            self.res.context_data.get('post').comments.all())

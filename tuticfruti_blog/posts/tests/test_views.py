# -*- coding: utf-8 -*-
import unittest

from django.core.urlresolvers import reverse
from django import test

from .. import models
from .. import views
from .. import factories
from tuticfruti_blog.core import data_fixtures


class TestViewBase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        data_fixtures.DataFixtures.load()

        # Posts
        cls.published_posts = models.Post.objects \
            .filter(status_id=models.Post.STATUS_PUBLISHED) \
            .order_by('-created')
        cls.published_post = models.Post.objects.get(slug='published-post')
        cls.draft_post = models.Post.objects.get(slug='draft-post')

        # Categories
        cls.enabled_categories = models.Category.objects \
            .filter(is_enabled=True) \
            .order_by('order')
        cls.python_category = models.Category.objects.get(slug='python')
        cls.first_category = models.Category.objects.get(slug='first-category')
        cls.disabled_category = models.Category.objects.get(
            slug='disabled-category')

        # Tags
        cls.tags = models.Tag.objects.all().order_by('term')
        cls.python_tag = models.Tag.objects.get(term='python')
        cls.django_tag = models.Tag.objects.get(term='django')
        cls.miscellaneous_tag = models.Tag.objects.get(term='miscellaneous')

        # Comments
        cls.published_post_comments = cls.published_post.comments \
            .filter(status_id=models.Comment.STATUS_PUBLISHED) \
            .order_by('-created')
        cls.pending_post_comments = cls.published_post.comments \
            .filter(status_id=models.Comment.STATUS_PENDING)


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

    def test_all_categories_are_sorted_and_enabled(self):
        categories = self.res.context_data.get('categories')

        for i in range(len(categories)):
            self.assertEqual(categories[i], self.enabled_categories[i])


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
        posts_expected = self.published_posts \
            .filter(categories__in=[self.python_category])
        posts = self.res.context_data.get('posts')

        for i in range(len(posts)):
            self.assertEqual(posts[i], posts_expected[i])


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
        posts_expected = self.published_posts \
            .filter(tags__in=[self.python_tag])
        self.res = self.client.get(
            reverse('posts:search'), dict(search_terms='PYTHON'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())

    def test_result_has_no_repeated(self):
        posts_expected = self.published_posts \
            .filter(tags__in=[self.python_tag]) \
            .distinct()
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms='python python'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())

    def test_restrict_result_by_category(self):
        posts_expected = models.Post.objects \
            .filter(categories__in=[self.python_category]) \
            .filter(tags__in=[self.python_tag, self.django_tag, self.miscellaneous_tag]) \
            .distinct()
        self.res = self.client.get(
            reverse(
                'posts:search_by_category',
                kwargs=dict(slug=self.python_category.slug)),
            dict(search_terms='python django miscellaneous'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())


class TestPostDetailView(TestViewBase):
    def setUp(self):
        self.res = self.client.get(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)))

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
        num_comments_expected = self.pending_post_comments.count()
        res = self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            dict(
                author='anonymous',
                email='anonymous@example.com',
                content=factories.FUZZY_TEXTS[0]),
            follow=True)
        num_comments = self.pending_post_comments.count()

        self.assertEqual(num_comments, num_comments_expected + 1)
        self.assertIn(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            res.redirect_chain[0][0])

    def test_send_an_invalid_form_comment(self):
        num_comments_expected = self.pending_post_comments.count()
        self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            dict(
                author=None,
                email=None,
                content=None))
        num_comments = self.pending_post_comments.count()

        self.assertEqual(num_comments, num_comments_expected)

    def test_comments_are_sorted_by_created_field(self):
        comments = self.res.context_data.get('post').comments.all()

        for i in range(len(comments)):
            self.assertEqual(comments[i], self.published_post_comments[i])

    def test_all_post_tags_are_sorted_by_alphabetical_order(self):
        tags = self.res.context_data.get('post').tags.all()

        for i in range(len(tags)):
            self.assertEqual(tags[i], self.tags[i])

    def test_all_categories_are_sorted_and_enabled(self):
        categories = self.res.context_data.get('post').categories.all()

        for i in range(len(categories)):
            self.assertEqual(categories[i], self.enabled_categories[i])

    def test_only_published_comments_are_counted(self):
        comments = self.res.context_data.get('post').comments.all()

        self.assertEqual(comments.count(), self.published_post_comments.count())

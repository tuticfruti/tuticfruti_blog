# -*- coding: utf-8 -*-
from unittest import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from .. import views
from .. import factories
from tuticfruti_blog.core import settings
from tuticfruti_blog.users.factories import UserFactory


class PostListViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):
        pass
        self.res = self.client.get(reverse('home'))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostListView.as_view().__name__)

    def test_object_list_in_context_data(self):
        self.assertIn('post_list', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/home.html', self.res.template_name)

    @mock.patch('tuticfruti_blog.posts.views.models.Post.objects.filter')
    def test_get_queryset_method(self, mock_filter):
        views.PostListView.get_queryset(mock.Mock(
            kwargs=dict(),
            request=mock.Mock(GET=dict())))

        self.assertIsNone(mock_filter.assert_called_once_with(status_id=settings.POST_PUBLIC_STATUS))

    #
    #   Integrated tests
    #

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=settings.POST_DRAFT_STATUS)

        res = self.client.get(reverse('home'))
        self.assertNotContains(res, post.title)

    def test_order_by_created_date(self):
        factories.PostFactory.create_batch(10, author=self.user, status_id=settings.POST_PUBLIC_STATUS)

        res = self.client.get(reverse('home'))
        posts = res.context_data.get('post_list')
        prev_post = None
        for post in posts:
            if prev_post:
                self.assertGreaterEqual(post.created, prev_post.created)
                prev_post = post


class PostListByCategoryViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()

    def setUp(self):
        self.res = self.client.get(
            reverse('posts:list_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)))

    #
    #   Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostListByCategoryView.as_view().__name__)

    def test_object_list_in_context_data(self):
        self.assertIn('post_list', self.res.context_data)

    def test_active_category_link_in_context_data(self):
        self.assertIsNotNone(self.res.context_data.get('current_category_id'))

    def test_template_name(self):
        self.assertIn('posts/home.html', self.res.template_name)

    def test_get_context_data_method(self):
        self.assertEqual(self.res.context_data.get('current_category_id'), settings.PYTHON_CATEGORY)

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test_get_queryset_method(self, mock_models):
        views.PostListByCategoryView.get_queryset(mock.Mock(
            kwargs=dict(category_id=settings.PYTHON_CATEGORY),
            request=mock.Mock(GET=dict())))

        self.assertIsNone(mock_models.Post.objects.filter.assert_called_once_with(
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.PYTHON_CATEGORY))

    #
    # Integrated tests
    #

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=settings.POST_DRAFT_STATUS)

        res = self.client.get(reverse('home', kwargs=dict()))
        self.assertNotContains(res, post.title)

        res = self.client.get(reverse('posts:list', kwargs=dict()))
        self.assertNotContains(res, post.title)

        res = self.client.get(reverse('posts:list_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)))
        self.assertNotContains(res, post.title)


class PostListSearchViewTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory()
        cls.terms = '{} {}'.format(settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY)

    def setUp(self):
        # /search?search_terms=python django
        self.res_search = self.client.get(
            reverse('posts:search'),
            dict(search_terms=self.terms))

        #<category_id>/search?search_terms=python django
        self.res_search_category = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms=self.terms))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res_search.status_code, 200)
        self.assertEqual(self.res_search_category.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res_search.resolver_match.func.__name__,
            views.PostListSearchView.as_view().__name__)
        self.assertEqual(
            self.res_search_category.resolver_match.func.__name__,
            views.PostListSearchView.as_view().__name__
        )

    def test_object_list_in_context_data(self):
        self.assertIn('post_list', self.res_search.context_data)
        self.assertIn('post_list', self.res_search_category.context_data)

    def test_active_category_link_in_context_data(self):
        self.assertIsNone(self.res_search.context_data.get('current_category_id'))
        self.assertIsNotNone(self.res_search_category.context_data.get('current_category_id'))

    def test_template_name(self):
        self.assertIn('posts/home.html', self.res_search.template_name)
        self.assertIn('posts/home.html', self.res_search_category.template_name)

    def test_get_context_data_method(self):
        self.assertIsNone(self.res_search.context_data.get('current_category_id'))
        self.assertEqual(
            self.res_search_category.context_data.get('current_category_id'),
            settings.PYTHON_CATEGORY)

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test_get_queryset_method(self, mock_models):
        views.PostListSearchView.get_queryset(mock.Mock(
            kwargs=dict(),
            request=mock.Mock(GET=dict(search_terms=self.terms))))

        self.assertIsNone(mock_models.Post.objects.filter.assert_called_once_with(
            status_id=settings.POST_PUBLIC_STATUS,
            tags__term__in=self.terms.split()))

        mock_models.reset_mock()
        views.PostListSearchView.get_queryset(mock.Mock(
            kwargs=dict(category_id=settings.PYTHON_CATEGORY),
            request=mock.Mock(GET=dict(search_terms=self.terms))))

        self.assertIsNone(mock_models.Post.objects.filter.assert_called_once_with(
            category_id=settings.PYTHON_CATEGORY,
            status_id=settings.POST_PUBLIC_STATUS,
            tags__term__in=self.terms.split()))

    def test_search_terms_in_context_data(self):
        terms = 'term1 term2 term3'
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms=terms))

        self.assertEqual(res.context_data.get('search_terms'), terms)
        self.assertContains(res, terms)

        res = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms=terms))

        self.assertEqual(res.context_data.get('search_terms'), terms)
        self.assertContains(res, terms)

    #
    # Integrated tests
    #

    def test_distinct_search_result(self):
        tag1 = factories.TagFactory()
        tag2 = factories.TagFactory()
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)
        post.tags.add(tag1, tag2)
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='{} {}'.format(tag1.term, tag2.term)))

        self.assertEqual(len(res.context_data['post_list']), 1)

    def test_search_category_filter_by_category(self):
        python_post = factories.PostFactory(
            author=self.user,
            category_id=settings.PYTHON_CATEGORY,
            status_id=settings.POST_PUBLIC_STATUS)
        django_post = factories.PostFactory(
            author=self.user,
            category_id=settings.DJANGO_CATEGORY,
            status_id=settings.POST_PUBLIC_STATUS)
        tag = factories.TagFactory()
        python_post.tags.add(tag)
        django_post.tags.add(tag)
        res = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms=tag.term))

        self.assertEqual(len(res.context_data['post_list']), 1)

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=settings.POST_DRAFT_STATUS)

        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='any_term'))
        self.assertNotContains(res, post.title)

        res = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms='any_term'))
        self.assertNotContains(res, post.title)

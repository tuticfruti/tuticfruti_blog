# -*- coding: utf-8 -*-
from unittest import mock

from django.core.urlresolvers import reverse
from django.test import SimpleTestCase, TestCase

from .. import views
from tuticfruti_blog.core import settings
from tuticfruti_blog.posts import models
from tuticfruti_blog.users.models import User


class PostListViewUnitTest(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.kwargs = dict(category_id=settings.PYTHON_CATEGORY)
        cls.terms = [settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY]

    def setUp(self):
        # Home page response
        self.res_home = self.client.get(reverse('home'))

        # Python category response
        self.res_category = self.client.get(
            reverse('posts:list', kwargs=dict(category_id=settings.PYTHON_CATEGORY)))

        # Searching terms response
        self.res_search = self.client.get(
            reverse('posts:search'),
            dict(search_terms='{} {}'.format(*self.terms)))

        # Searching terms with python category response
        self.res_search_category = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms='{} {}'.format(*self.terms)))

    def test_http_request_ok(self):
        self.assertEqual(self.res_home.status_code, 200)
        self.assertEqual(self.res_category.status_code, 200)
        self.assertEqual(self.res_search.status_code, 200)
        self.assertEqual(self.res_search_category.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res_home.resolver_match.func.__name__,
            views.PostListView.as_view().__name__)
        self.assertEqual(
            self.res_category.resolver_match.func.__name__,
            views.PostListView.as_view().__name__)
        self.assertEqual(
            self.res_search.resolver_match.func.__name__,
            views.PostListView.as_view().__name__)
        self.assertEqual(
            self.res_search_category.resolver_match.func.__name__,
            views.PostListView.as_view().__name__
        )

    def test_object_list_in_context_data(self):
        self.assertIn('post_list', self.res_home.context_data)
        self.assertIn('post_list', self.res_category.context_data)
        self.assertIn('post_list', self.res_search.context_data)
        self.assertIn('post_list', self.res_search_category.context_data)

    def test_active_category_link_in_context_data(self):
        self.assertIsNone(self.res_home.context_data.get('current_category_id'))
        self.assertIsNotNone(self.res_category.context_data.get('current_category_id'))
        self.assertIsNone(self.res_search.context_data.get('current_category_id'))
        self.assertIsNotNone(self.res_search_category.context_data.get('current_category_id'))

    def test_template_name(self):
        self.assertIn('posts/home.html', self.res_home.template_name)
        self.assertIn('posts/home.html', self.res_category.template_name)
        self.assertIn('posts/home.html', self.res_search.template_name)
        self.assertIn('posts/home.html', self.res_search_category.template_name)

    def test_get_context_data_method(self):
        self.assertIsNone(self.res_home.context_data.get('current_category_id'))
        self.assertEqual(
            self.res_category.context_data.get('current_category_id'),
            settings.PYTHON_CATEGORY)
        self.assertIsNone(self.res_search.context_data.get('current_category_id'))
        self.assertEqual(
            self.res_search_category.context_data.get('current_category_id'),
            settings.PYTHON_CATEGORY)

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test_get_queryset_method(self, mock_models):
        mock_models.Post.objects.all.return_value = mock.sentinel.all
        mock_models.Post.objects.filter.return_value = mock.sentinel.filter

        kwargs = [
            dict(),
            dict(category_id=settings.PYTHON_CATEGORY),
            dict(),
            dict(category_id=settings.PYTHON_CATEGORY)]

        requests = [
            mock.Mock(GET=dict()),
            mock.Mock(GET=dict()),
            mock.Mock(GET=dict(search_terms=self.terms)),
            mock.Mock(GET=dict(search_terms=self.terms))]

        return_values = [
            mock.sentinel.all,
            mock.sentinel.filter,
            mock.sentinel.search,
            mock.sentinel.search]

        for i in range(len(kwargs)):
            mockPostListView = mock.Mock(
                kwargs=kwargs[i],
                request=requests[i],
                _get_queryset_by_tags=mock.Mock(return_value=mock.sentinel.search))
            return_value = views.PostListView.get_queryset(mockPostListView)
            self.assertEqual(return_value, return_values[i])

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test__get_queryset_by_tags(self, mock_models):
        mockPostListView = mock.Mock(
            kwargs=dict(),
            request=mock.Mock(GET=dict(search_terms='{} {}'.format(*self.terms))))

        views.PostListView._get_queryset_by_tags(mockPostListView)
        self.assertEqual(mock.call(tags__term__in=self.terms), mock_models.Post.objects.filter.call_args)

        views.PostListView._get_queryset_by_tags(mockPostListView, category_id=settings.PYTHON_CATEGORY)
        self.assertEqual(
            mock.call(category_id=settings.PYTHON_CATEGORY, tags__term__in=self.terms),
            mock_models.Post.objects.filter.call_args)

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


class PostListViewIntegratedTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='tuticfruti',
            email='tuticfruti@example.com',
            password='1234')

        cls.python_post = models.Post.objects.create(
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            category_id=settings.PYTHON_CATEGORY,
            author=cls.user)
        cls.django_post = models.Post.objects.create(
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            category_id=settings.DJANGO_CATEGORY,
            author=cls.user)
        cls.miscellaneous_post = models.Post.objects.create(
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            category_id=settings.MISCELLANEOUS_CATEGORY,
            author=cls.user)
        cls.python_tag = cls.python_post.tags.create(term=settings.PYTHON_CATEGORY)
        cls.distinct_tag = cls.python_post.tags.create(term='distinct')
        cls.django_tag = cls.django_post.tags.create(term=settings.DJANGO_CATEGORY)
        cls.miscellaneous_tag = cls.miscellaneous_post.tags.create(term=settings.MISCELLANEOUS_CATEGORY)

    def test_search_queryset_result_without_category(self):
        # Search terms without category param and one search term
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms=settings.PYTHON_CATEGORY))

        self.assertContains(res, self.python_post.title)
        self.assertEqual(len(res.context_data['post_list']), 1)

        # Search terms without category param and twice search terms
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='{} {}'.format(settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY)))

        self.assertContains(res, self.python_post.title)
        self.assertContains(res, self.django_post.title)
        self.assertEqual(len(res.context_data['post_list']), 2)

    def test_search_category_queryset_result_with_category(self):
        res = self.client.get(
            reverse('posts:search_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms='{} {} {}'.format(
                settings.PYTHON_CATEGORY,
                settings.DJANGO_CATEGORY,
                settings.MISCELLANEOUS_CATEGORY)))

        self.assertContains(res, self.python_post.title)
        self.assertEqual(len(res.context_data['post_list']), 1)

    def test_distinct_search_result(self):
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='{} {}'.format(settings.PYTHON_CATEGORY, 'distinct')))

        self.assertContains(res, self.python_post.title)
        self.assertEqual(len(res.context_data['post_list']), 1)

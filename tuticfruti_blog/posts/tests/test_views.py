# -*- coding: utf-8 -*-
from unittest import mock

from django.test import TestCase
from django.core.urlresolvers import reverse

from .. import views
from tuticfruti_blog.core.settings import PYTHON_CATEGORY, CATEGORY_CHOICES


class PostListViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        cls.categories_ids = [category_id for category_id, category_name in CATEGORY_CHOICES]
        cls.python_kwargs = dict(category_id=PYTHON_CATEGORY)
        cls.empty_kwargs = dict()

    def setUp(self):
        self.response = self.client.get(reverse('posts:list', kwargs=self.python_kwargs))

    @mock.patch('tuticfruti_blog.posts.views.models.Post.objects.all', return_value=mock.sentinel.all_return_value)
    @mock.patch('tuticfruti_blog.posts.views.models.Post.objects.filter', return_value=mock.sentinel.filter_return_value)
    def test_get_queryset(self, mock_filter, mock_all):
        queryset = views.PostListView.get_queryset(mock.Mock(
            spec=views.PostListView,
            kwargs=self.empty_kwargs))
        self.assertIsNone(mock_all.assert_called_once_with())
        self.assertEqual(queryset, mock.sentinel.all_return_value)

        queryset = views.PostListView.get_queryset(mock.Mock(
            spec=views.PostListView,
            kwargs=self.python_kwargs))
        self.assertIsNone(mock_filter.assert_called_once_with(category_id=PYTHON_CATEGORY))
        self.assertEqual(queryset, mock.sentinel.filter_return_value)

    @mock.patch('tuticfruti_blog.posts.views.ListView.get_context_data')
    def test_get_context_data(self, mock_super_get_context_data):
        mock_super_get_context_data.return_value = dict(context_var=mock.sentinel.context_var)
        context_data = views.PostListView.get_context_data(mock.Mock(
            spec=views.PostListView,
            kwargs=self.python_kwargs))
        self.assertEqual(mock.sentinel.context_var, context_data.get('context_var'))

    def test_status_code_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_object_list_in_context_data(self):
        self.assertIn('post_list', self.response.context_data)

    def test_active_category_link_in_context_data(self):
        self.assertEqual(self.response.context_data.get('current_category_id'), PYTHON_CATEGORY)

    def test_template_name(self):
        self.assertIn('posts/home.html', self.response.template_name)

    def test_url_conf_resolver(self):
        self.assertEqual(self.response.resolver_match.func.__name__, views.PostListView.as_view().__name__)

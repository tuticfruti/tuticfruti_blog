# -*- coding: utf-8 -*-
from unittest import mock

from django.test import TestCase

from ..views import HomePageView, PostListView, BaseListView


class BaseListViewTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(BaseListView, cls).setUpClass()
        #...

    @classmethod
    def tearDownClass(cls):
        super(BaseListViewTest, cls).setUpClass()
        # ...

    @classmethod
    def setUpTestData(cls):
        pass
        # Create rows class level
        # cls.row = Model.objects.create()

    def setUp(self):
        # Create rows test level
        pass

    def test_template_name(self):
        self.assertEqual(BaseListView.template_name, 'posts/home.html')

    def test_context_object_name(self):
        self.assertEqual(BaseListView.context_object_name, 'post_list')

    def test_paginate_by(self):
        self.assertEqual(BaseListView.paginate_by, 10)

    def test_ordering(self):
        self.assertEqual(BaseListView.ordering, '-created')


class HomePageViewTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/')

    def test_correct_view(self):
        self.assertEqual(self.response.resolver_match.func.__name__, HomePageView.as_view().__name__)


class PostListViewTest(TestCase):
    def test_correct_view(self):
        self.response = self.client.get('/posts/category/python/')
        self.assertEqual(self.response.resolver_match.func.__name__, PostListView.as_view().__name__)

    def test_categories_links(self):
        pass

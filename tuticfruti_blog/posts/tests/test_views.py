# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test import RequestFactory

from ..views import HomePageView, PostListView
from ..models import Post


class PostListViewTest(TestCase):

    def setUp(self):
        self.categories_ids = [category_id for category_id, category_name in Post.CATEGORIES]
        Post.objects.create(title='Post title', category_id=Post.PYTHON_CATEGORY)

    def test_current_category_is_in_context(self):
        response = self.client.get(reverse('posts:list', kwargs={'category_id': Post.PYTHON_CATEGORY}))
        self.assertIsNotNone(
            response.context_data.get('current_category_id', None),
            "Variable current_category_id doesn't exist in context")
        self.assertIn(response.context_data.get('current_category_id'), self.categories_ids)

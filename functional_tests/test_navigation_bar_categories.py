# -*- coding: utf-8 -*-
from .pages import HomePage
from .base import FunctionalTest
from tuticfruti_blog.core.settings import PYTHON_CATEGORY, DJANGO_CATEGORY, MISCELLANEOUS_CATEGORY
from tuticfruti_blog.posts import models


class NavigationBarCategoriesTest(FunctionalTest):

    def setUp(self):
        self.home_page = HomePage(self.live_server_url)

    def test_current_active_category(self):
        self.home_page.load()

        # Firs time, all categories are disabled
        self.assertFalse(self.home_page.python_category_link.is_active())
        self.assertFalse(self.home_page.django_category_link.is_active())
        self.assertFalse(self.home_page.miscellaneous_category_link.is_active())

        # User clicks Python link
        self.home_page.python_category_link.click()
        self.assertTrue(self.home_page.python_category_link.is_active())

        # User clicks Python link
        self.home_page.django_category_link.click()
        self.assertTrue(self.home_page.django_category_link.is_active())

        # User clicks Python link
        self.home_page.miscellaneous_category_link.click()
        self.assertTrue(self.home_page.miscellaneous_category_link.is_active())

        # User clicks Home link
        self.home_page.home_link.click()
        self.assertFalse(self.home_page.python_category_link.is_active())
        self.assertFalse(self.home_page.django_category_link.is_active())
        self.assertFalse(self.home_page.miscellaneous_category_link.is_active())

    def test_filter_by_category_id(self):
        models.Post.objects.create(
            title='Post title {}'.format(PYTHON_CATEGORY),
            category_id=PYTHON_CATEGORY)
        models.Post.objects.create(
            title='Post title {}'.format(DJANGO_CATEGORY),
            category_id=DJANGO_CATEGORY)
        models.Post.objects.create(
            title='Post title {}'.format(MISCELLANEOUS_CATEGORY),
            category_id=MISCELLANEOUS_CATEGORY)

        self.home_page.load()

        # User clicks on Python link
        self.home_page.python_category_link.click()
        self.assertEqual(len(self.home_page.posts), 1)

        # User clicks on Django link
        self.home_page.django_category_link.click()
        self.assertEqual(len(self.home_page.posts), 1)

        # User clicks on Miscellaneous link
        self.home_page.miscellaneous_category_link.click()
        self.assertEqual(len(self.home_page.posts), 1)

        # User come back to home page
        self.home_page.home_link.click()
        self.assertEqual(len(self.home_page.posts), 3)

# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from .pages import HomePage
from .base import FunctionalTest
from tuticfruti_blog.posts.models import Post


class NavigationBarTest(FunctionalTest):

    def test_active_category(self):
        # Firs time, all categories are disabled
        home_page = HomePage(self.live_server_url)
        home_page.load()
        self.assertFalse(home_page.python_category_link.is_enabled())
        self.assertFalse(home_page.django_category_link.is_enabled())
        self.assertFalse(home_page.miscellaneous_category_link.is_enabled())

        # User clicks Python link
        home_page.python_category_link.click()
        self.assertTrue(home_page.python_category_link.is_enabled())

        # User clicks Python link
        home_page.django_category_link.click()
        self.assertTrue(home_page.django_category_link.is_enabled())

        # User clicks Python link
        home_page.python_miscellaneous_link.click()
        self.assertTrue(home_page.miscellaneous_category_link.is_enabled())

        # User clicks Home link
        home_page.home_link.click()
        self.assertFalse(home_page.python_category_link.is_enabled())
        self.assertFalse(home_page.django_category_link.is_enabled())
        self.assertFalse(home_page.miscellaneous_category_link.is_enabled())

    def test_user_click_on_all_categories(self):
        Post.objects.create(
            title='Post title {}'.format(Post.PYTHON_CATEGORY),
            category_id=Post.PYTHON_CATEGORY)
        Post.objects.create(
            title='Post title {}'.format(Post.DJANGO_CATEGORY),
            category_id=Post.DJANGO_CATEGORY)
        Post.objects.create(
            title='Post title {}'.format(Post.MISCELLANEOUS_CATEGORY),
            category_id=Post.MISCELLANEOUS_CATEGORY)

        # User clicks on Python link
        home_page = HomePage(self.live_server_url)
        home_page.load()
        home_page.python_category_link.click()
        self.assertEqual(len(home_page.posts), 1)

        # User clicks on Django link
        home_page.django_category_link.click()
        self.assertEqual(len(home_page.posts), 1)

        # User clicks on Miscellaneous link
        home_page.miscellaneous_category_link.click()
        self.assertEqual(len(home_page.posts), 1)

        # User come back to home page
        home_page.home_link.click()
        self.assertEqual(len(home_page.posts), 3)

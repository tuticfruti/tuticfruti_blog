# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse

from .pages import HomePage
from .base import FunctionalTest
from tuticfruti_blog.posts.models import Post


class NavigationBarTest(FunctionalTest):

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
        home_page.go_to()
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

# -*- coding: utf-8 -*-
from selenium import webdriver

from .pom.pages.home_page import HomePage
from .base import FunctionalTest

from tuticfruti_blog.core import settings
from tuticfruti_blog.posts import models
from tuticfruti_blog.users.models import User


class NavigationBarCategoriesTest(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='tuticfruti',
            email='tuticfruti@example.com',
            password='1234')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.home_page = HomePage(self.driver, self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def test_current_active_category(self):
        # Firs time, all categories are disabled
        self.assertFalse(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

        # User selects Python category
        self.home_page.select_category(settings.PYTHON_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))

        # User selects Django category
        self.home_page.select_category(settings.DJANGO_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))

        # User selects Miscellaneous category
        self.home_page.select_category(settings.MISCELLANEOUS_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

        # User come back to Home page
        self.home_page.goto_home_page()
        self.assertFalse(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

    def test_filter_by_category_id(self):
        models.Post.objects.create(
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            category_id=settings.PYTHON_CATEGORY,
            author=self.user)
        models.Post.objects.create(
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            category_id=settings.DJANGO_CATEGORY,
            author=self.user)
        models.Post.objects.create(
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            category_id=settings.MISCELLANEOUS_CATEGORY,
            author=self.user)

        # User selects Python category
        self.home_page.select_category(settings.PYTHON_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User selects Django category
        self.home_page.select_category(settings.DJANGO_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User selects Miscellaneous category
        self.home_page.select_category(settings.MISCELLANEOUS_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User come back to Home page
        self.home_page.goto_home_page()
        self.assertEqual(self.home_page.count_posts(), 3)

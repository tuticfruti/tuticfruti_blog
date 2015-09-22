# -*- coding: utf-8 -*-
from selenium import webdriver

from .pom import pages
from .base import FunctionalTest

from tuticfruti_blog.core import settings
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.posts import factories


class NavigationBarCategoriesTest(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.user = UserFactory()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        self.home_page = pages.HomePage(self.driver, self.live_server_url)

    def tearDown(self):
        pass

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
        factories.PostFactory(
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.PYTHON_CATEGORY,
            author=self.user)
        factories.PostFactory(
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.DJANGO_CATEGORY,
            author=self.user)
        factories.PostFactory(
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
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

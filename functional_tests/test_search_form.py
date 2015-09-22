# -*- coding: utf-8 -*-
from selenium import webdriver

from django.core.urlresolvers import reverse

from .base import FunctionalTest
from .pom import pages
from tuticfruti_blog.posts import factories
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.core import settings


class SearchFormTest(FunctionalTest):
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

    def test_search_terms_with_and_without_category_selected(self):
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.PYTHON_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.PYTHON_CATEGORY)])
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.DJANGO_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.DJANGO_CATEGORY)])
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.MISCELLANEOUS_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.MISCELLANEOUS_CATEGORY)])
        self.home_page.reload()

        # User searchs on All posts
        terms = '{} {}'.format(settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY)
        self.home_page.search_posts(terms)
        self.assertEqual(self.home_page.count_posts(), 2)

        # User searchs on Python posts
        self.home_page.search_posts(terms, category_id=settings.PYTHON_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User searchs on Django posts
        self.home_page.search_posts(terms, category_id=settings.DJANGO_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User searchs on Miscellaneous posts
        terms = '{} {}'.format(settings.PYTHON_CATEGORY, settings.MISCELLANEOUS_CATEGORY)
        self.home_page.search_posts(terms, category_id=settings.MISCELLANEOUS_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

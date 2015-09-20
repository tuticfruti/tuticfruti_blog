# -*- coding: utf-8 -*-
from selenium import webdriver

from django.core.urlresolvers import reverse

from .base import FunctionalTest
from .pom.pages.home_page import HomePage
from tuticfruti_blog.posts import models
from tuticfruti_blog.users.models import User
from tuticfruti_blog.core import settings


class SearchFormTest(FunctionalTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(
            username='tuticfruti',
            email='tuticfruti@example.com',
            password='1234')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.home_page = HomePage(self.driver, self.live_server_url + reverse('home'))

    def tearDown(self):
        self.driver.quit()

    def test_search_terms_with_and_without_category_selected(self):
        python_post = models.Post.objects.create(
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            category_id=settings.PYTHON_CATEGORY,
            author=self.user)
        python_post.tags.create(term=settings.PYTHON_CATEGORY)

        django_post = models.Post.objects.create(
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            category_id=settings.DJANGO_CATEGORY,
            author=self.user)
        django_post.tags.create(term=settings.DJANGO_CATEGORY)

        miscellaneous_post = models.Post.objects.create(
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            category_id=settings.MISCELLANEOUS_CATEGORY,
            author=self.user)
        miscellaneous_post.tags.create(term=settings.MISCELLANEOUS_CATEGORY)
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

# -*- coding: utf-8 -*-
from selenium import webdriver

from .base import FunctionalTest
from .pom import pages
from tuticfruti_blog.posts import factories
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.core import settings


class PostDetailsTest(FunctionalTest):
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

    def test_post_fields(self):
        post_db = factories.PostFactory(
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user,
            tags=factories.TagFactory.build_batch(2))

        self.home_page.reload()
        post_element = self.home_page.get_post_details(0)

        self.assertEqual(post_element.get('title'), post_db.title)
        self.assertEqual(post_element.get('created'), post_db.created.strftime('%B %d, %Y'))
        self.assertEqual(post_element.get('tags'), 'term0, term1,')
        self.assertEqual(post_element.get('content'), post_db.content)

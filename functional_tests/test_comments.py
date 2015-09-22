# -*- coding: utf-8 -*-
from unittest import skip

from selenium import webdriver

from functional_tests.pom import pages
from .base import FunctionalTest
from tuticfruti_blog.core import settings
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.posts import factories


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
        pass

    def tearDown(self):
        pass

    def test_create_new_comment(self):
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)
        comment = factories.CommentFactory()
        home_page = pages.HomePage(self.driver, self.live_server_url)

        # User click on a post Read more ... link
        home_page.goto_post(post.title)

        # User enter comment details (name, email and comment) and send them
        post_page = pages.PostPage(self.driver, home_page.current_url)
        post_page.send_comment_form(comment)

        self.assertTrue(post_page.is_comment_displayed(comment.content))

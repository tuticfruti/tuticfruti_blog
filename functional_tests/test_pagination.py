# -*- coding: utf-8 -*-
from selenium import webdriver

from .pom import pages
from .base import FunctionalTest

from tuticfruti_blog.core import settings
from tuticfruti_blog.posts import factories
from tuticfruti_blog.users.factories import UserFactory


class PaginationTest(FunctionalTest):
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

    def test_empty_page(self):
        self.assertTrue(self.home_page.is_empty_message_visible())

    def test_orphans_posts(self):
        factories.PostFactory.create_batch(
            settings.PAGINATE_BY + 1,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)
        self.home_page.reload()

        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY + 1)

    def test_max_number_of_posts_per_page(self):
        factories.PostFactory.create_batch(
            settings.PAGINATE_BY + 2,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)
        self.home_page.reload()

        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY)

    def test_prev_next_buttons(self):
        factories.PostFactory.create_batch(
            3*settings.PAGINATE_BY,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)
        self.home_page.reload()

        # Prev page link is not visible
        self.assertFalse(self.home_page.is_prev_link_visible())

        # User go to Next page twice
        self.home_page.goto_next_page()
        self.home_page.goto_next_page()
        self.assertEqual(self.home_page.current_page, 3)

        # Next page link is not visible
        self.assertFalse(self.home_page.is_next_link_visible())

        # User come back to home page
        self.home_page.goto_prev_page()
        self.home_page.goto_prev_page()
        self.assertEqual(self.home_page.current_page, 1)

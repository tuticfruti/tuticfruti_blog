# -*- coding: utf-8 -*-
from selenium import webdriver

from .pom.pages.home_page import HomePage
from .base import FunctionalTest

from tuticfruti_blog.core import settings
from tuticfruti_blog.posts.models import Post
from tuticfruti_blog.users.models import User


class PaginationTest(FunctionalTest):
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

    def test_empty_page(self):
        self.assertTrue(self.home_page.is_empty_message_visible())

    def test_orphans_posts(self):
        for i in range(settings.PAGINATE_BY + 1):
            Post.objects.create(title='Post title {}'.format(i), author=self.user)
        self.home_page.reload()
        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY + 1)

    def test_max_number_of_posts_per_page(self):
        for i in range(settings.PAGINATE_BY + 2):
            Post.objects.create(title='Post title {}'.format(i), author=self.user)
        self.home_page.reload()
        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY)

    def test_prev_next_buttons(self):
        for i in range(3*settings.PAGINATE_BY):
            Post.objects.create(title='Post title {}'.format(i), author=self.user)
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

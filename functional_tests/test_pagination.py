# -*- coding: utf-8 -*-
from .pages import HomePage
from .base import FunctionalTest
from tuticfruti_blog.core.settings import PAGINATE_BY
from tuticfruti_blog.posts.models import Post
from tuticfruti_blog.core.exceptions import ElementNotFoundError


class PaginationTest(FunctionalTest):
    def setUp(self):
        self.home_page = HomePage(self.live_server_url)

    def test_empty_page(self):
        self.home_page.load()
        self.assertTrue('Results were not found.' in self.home_page.container.get_text())

    def test_orphans_posts(self):
        for i in range(PAGINATE_BY + 1):
            Post.objects.create(title='Post title {}'.format(i))
        self.home_page.load()
        self.assertEqual(len(self.home_page.posts), PAGINATE_BY + 1)

    def test_max_number_of_posts_per_page(self):
        for i in range(PAGINATE_BY + 2):
            Post.objects.create(title='Post title {}'.format(i))
        self.home_page.load()
        self.assertEqual(len(self.home_page.posts), PAGINATE_BY)

    def test_prev_next_buttons(self):
        for i in range(3*PAGINATE_BY):
            Post.objects.create(title='Post title {}'.format(i))
        self.home_page.load()

        # User can't click on pagination Prev link
        with self.assertRaises(ElementNotFoundError):
            self.home_page.pagination_prev_link.click()

        # User clicks on pagination Next link twice
        self.home_page.pagination_next_link.click()
        self.home_page.pagination_next_link.click()
        self.assertIn('?page=3', self.home_page.get_current_url())

        # User can't click on pagination Next link
        with self.assertRaises(ElementNotFoundError):
            self.home_page.pagination_next_link.click()

        # User come back to home page
        self.home_page.pagination_prev_link.click()
        self.home_page.pagination_prev_link.click()
        self.assertIn('?page=1', self.home_page.get_current_url())

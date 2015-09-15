# -*- coding: utf-8 -*-
from selenium import webdriver

from django.utils import timezone

from .base import FunctionalTest
from .pom.pages.home_page import HomePage
from tuticfruti_blog.posts import models


class PostDetailsTest(FunctionalTest):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.home_page = HomePage(self.driver, self.live_server_url)

    def tearDown(self):
        self.driver.quit()

    def test_post_fields(self):
        post_db = models.Post.objects.create(
            title='Post title',
            tags='tag1 tag2')
        self.home_page.reload()
        post_element = self.home_page.get_post_details(0)

        self.assertEqual(post_element.get('title'), post_db.title)
        self.assertEqual(post_element.get('created'), post_db.created.strftime('%B %d, %Y'))
        self.assertEqual(post_element.get('tags'), post_db.tags)
        self.assertEqual(post_element.get('content'), post_db.content)

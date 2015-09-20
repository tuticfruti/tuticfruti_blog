# -*- coding: utf-8 -*-
from selenium import webdriver

from .base import FunctionalTest
from .pom.pages.home_page import HomePage
from tuticfruti_blog.posts import models
from tuticfruti_blog.users.models import User


class PostDetailsTest(FunctionalTest):
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

    def test_post_fields(self):
        post_db = models.Post.objects.create(
            title='Post title',
            author=self.user)
        post_db.tags.create(term='tag1')
        post_db.tags.create(term='tag2')
        self.home_page.reload()
        post_element = self.home_page.get_post_details(0)

        self.assertEqual(post_element.get('title'), post_db.title)
        self.assertEqual(post_element.get('created'), post_db.created.strftime('%B %d, %Y'))
        self.assertEqual(post_element.get('tags'), 'tag1, tag2,')
        self.assertEqual(post_element.get('content'), post_db.content)

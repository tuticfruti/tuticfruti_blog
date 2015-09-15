# -*- coding: utf-8 -*-
from django.utils import timezone

from .base import FunctionalTest
from .pages import HomePage
from tuticfruti_blog.posts import models


class PostDetailsTest(FunctionalTest):

    def setUp(self):
        models.Post.objects.create(
            title='Post title')
        self.home_page = HomePage(self.live_server_url)
        self.home_page.load()

    def test_post_fields(self):
        self.assertEqual(
            self.home_page.posts[0].find_by_class_name('post-title').text,
            'Post title')
        self.assertEqual(
            self.home_page.posts[0].find_by_class_name('post-created').text,
            timezone.now())

# -*- coding: utf-8 -*-
import datetime

from selenium.common.exceptions import NoSuchElementException

from django.utils import timezone

from functional_tests.pom import pages
from .base_page import FunctionalTest
from tuticfruti_blog.core import settings
from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.posts import factories
from tuticfruti_blog.posts import models


class PostDetailPageTest(FunctionalTest):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED,
            content=data_fixtures.FUZZY_TEXTS[5])
        self.post_details_page = pages.PostDetailsPage(self.live_server_url, self.post.slug)
        self.post_details_page.open()

    def tearDown(self):
        self.post_details_page.close()

    def test_comments_order(self):
        comment = factories.CommentFactory(
            post=self.post, status_id=models.Comment.STATUS_PUBLISHED)
        another_comment = factories.CommentFactory(
            post=self.post, status_id=models.Comment.STATUS_PUBLISHED)

        comment.created = datetime.datetime(2015, 1, 1, tzinfo=timezone.get_current_timezone())
        comment.save()
        another_comment.created = datetime.datetime(
            2015, 2, 1, tzinfo=timezone.get_current_timezone())
        another_comment.save()
        self.post_details_page.reload()

        self.assertTrue(
            'February' in self.post_details_page.get_comment_details_by_key(0).get('created'))

    def test_comment_details(self):
        comment = factories.CommentFactory(
            post=self.post,
            status_id=models.Comment.STATUS_PUBLISHED,
            author='anonymous',
            email='anonymous@example.com',
            content='Comment content')

        self.post_details_page.reload()
        comment_element = self.post_details_page.get_comment_details_by_pk(comment.pk)

        self.assertEqual(comment_element.get('created'), comment.created.strftime('%B %d, %Y'))
        self.assertEqual(comment_element.get('author'), comment.author)
        self.assertEqual(comment_element.get('content'), comment.content)

    def test_all_comments_are_present_comments(self):
        factories.CommentFactory.create_batch(
            5, post=self.post, status_id=models.Comment.STATUS_PUBLISHED)
        self.post_details_page.reload()

        self.assertEqual(self.post_details_page.count_comments(), 5)

    def test_empty_comments_message(self):
        self.assertTrue(self.post_details_page.is_empty_message_visible())

    def test_post_content_is_not_truncated(self):
        post_element = self.post_details_page.get_post_details()

        self.assertEqual(len(self.post.content), len(post_element.get('content')))

    def test_post_details(self):
        self.post.tags.add(
            factories.TagFactory(term='term0'),
            factories.TagFactory(term='term1'))
        factories.CommentFactory.create_batch(
            5, post=self.post, status_id=models.Comment.STATUS_PUBLISHED)

        self.post_details_page.reload()
        post_element = self.post_details_page.get_post_details()

        self.assertEqual(post_element.get('author'), self.post.author.username)
        self.assertEqual(post_element.get('title'), self.post.title)
        self.assertEqual(post_element.get('num_comments'), str(5))
        self.assertEqual(post_element.get('created'), self.post.created.strftime('%B %d, %Y'))
        self.assertEqual(post_element.get('tags'), 'term0 term1')
        self.assertHTMLEqual(post_element.get('content'), self.post.content)

    def test_send_new_comment(self):
        url_prev = self.post_details_page.current_driver_url
        self.post_details_page.send_comment_form(
            author='author',
            email='author@example.com',
            content='Content ...')

        self.assertEqual(self.post.comments.count(), 1)
        self.assertEqual(url_prev, self.post_details_page.current_driver_url)

    def test_only_public_comments_are_displayed(self):
        comment = factories.CommentFactory(
            post=self.post, status_id=models.Comment.STATUS_PENDING)

        self.post_details_page.reload()

        with self.assertRaises(NoSuchElementException):
            self.post_details_page.get_comment_details_by_pk(comment.pk)

    def test_new_comments_default_status_is_pending(self):
        self.fail('test_new_comments_default_status_is_pending FAULT')

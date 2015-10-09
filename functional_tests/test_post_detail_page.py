# -*- coding: utf-8 -*-
import unittest
import re

from django.core.urlresolvers import reverse

from . import functional_test
from .pom import pages

from tuticfruti_blog.posts import factories
from tuticfruti_blog.posts import models


class TestPostDetailPage(functional_test.FunctionalTest):
    def setUp(self):
        super().setUpTestData()
        self.page = pages.PostDetailsPage(
            self.live_server_url, self.published_post.slug)
        self.page.open()

    def tearDown(self):
        self.page.close()

    def test_post_detail(self):
        post_expected = self.published_post

        search_result = re.search(models.Post.HR, post_expected.content)
        if search_result:
            content_expected = post_expected.content[search_result.start() + len(models.Post.HR):]
        else:
            content_expected = post_expected.content

        categories_expected = post_expected.categories.all_enabled().values_list('name', flat=True)
        tags_expected = post_expected.tags.all().values_list('term', flat=True)
        comments_expected = self.published_post_comments
        date_expected = '{dt:%B} {dt.day}, {dt.year}'.format(dt=post_expected.created)

        post = self.page.get_post_details()

        self.assertEqual(post.get('id'), post_expected.id)
        self.assertEqual(post.get('pk'), post_expected.pk)
        self.assertEqual(post.get('author'), post_expected.author.username)
        self.assertEqual(post.get('title'), post_expected.title)
        self.assertEqual(post.get('num_comments'), str(comments_expected.count()))
        self.assertEqual(post.get('created'), date_expected)
        self.assertEqual(post.get('tags'), ' '.join(tags_expected))
        self.assertEqual(post.get('categories'), ' '.join(categories_expected))
        self.assertHTMLEqual(post.get('content'), content_expected)

    def test_comments_sorted_by_created_field(self):
        comment_expected = factories.CommentFactory(
            post=self.published_post,
            status_id=models.Comment.STATUS_PUBLISHED)
        self.page.reload()
        comment = self.page.get_comment_details_by_key(0)

        self.assertEqual(comment.get('pk'), comment_expected.pk)

    def test_comment_details(self):
        comment = self.page.get_comment_details_by_pk(
            self.published_comment.pk)

        self.assertEqual(
            comment.get('created'),
            '{dt:%B} {dt.day}, {dt.year}'.format(dt=self.published_comment.created))
        self.assertEqual(comment.get('author'), self.published_comment.author)
        self.assertEqual(comment.get('content'), self.published_comment.content)

    def test_all_comments_are_displayed(self):
        self.assertEqual(self.page.count_comments(), 10)

    def test_empty_comments_message(self):
        self.published_post.comments.all().delete()
        self.page.reload()

        self.assertTrue(self.page.is_empty_message_visible())

    def test_post_content_is_not_truncated(self):
        post_expected = self.published_post
        search_result = re.search(models.Post.HR, post_expected.content)
        if search_result:
            content_expected = post_expected.content[:search_result.start()]
        else:
            content_expected = post_expected.content
        content = self.page.get_post_details().get('content')

        self.assertEqual(len(content), len(content_expected))

    def test_send_new_comment(self):
        url_expected = self.page.current_driver_url
        self.page.send_comment_form(
            author='test_send_new_comment',
            email='test_send_new_comment@example.com',
            content='Comment sent ...')
        self.page.reload()
        url = self.page.current_driver_url
        num_comments = self.page.count_comments()

        # Comments for published_post increments by 1
        self.assertEqual(num_comments, self.published_post_comments.count())
        # Send a comment redirects user to the same post page
        self.assertEqual(url, url_expected)
        # New comment is pending and not visible
        self.assertNotEqual(
            self.page.get_comment_details_by_key(0).get('author'),
            'test_send_new_comment')

    def test_tag_link(self):
        self.page.click_on_tag_by_text(self.python_tag.term)
        self.assertIn(
            '{}{}'.format(
                reverse('posts:search'),
                '?search_terms={}'.format(self.python_tag.term)),
            self.page.current_driver_url)

    def test_category_link(self):
        self.page.click_on_category_by_text(self.python_category.name)
        self.assertIn(
            reverse(
                'posts:list_by_category',
                kwargs=dict(slug=self.python_category.slug)),
            self.page.current_driver_url)

# -*- coding: utf-8 -*-
import datetime

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

    def test_post_details(self):
        post_element = self.page.get_post_details()

        self.assertEqual(post_element.get('id'), self.published_post.id)
        self.assertEqual(post_element.get('pk'), self.published_post.pk)
        self.assertEqual(
            post_element.get('author'), self.published_post.author.username)
        self.assertEqual(post_element.get('title'), self.published_post.title)
        self.assertEqual(post_element.get('num_comments'), str(10))
        self.assertEqual(
            post_element.get('created'),
            '{dt:%B} {dt.day}, {dt.year}'.format(dt=self.published_post.created))
        self.assertEqual(
            post_element.get('tags'),
            ' '.join(self.published_post.tags.all().values_list('term', flat=True)))
        self.assertEqual(
            post_element.get('categories'),
            ' '.join(self.published_post.categories.all_enabled().values_list('name', flat=True)))
        self.assertHTMLEqual(
            post_element.get('content'),
            self.published_post.content)

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
        self.assertEqual(comment.get('email'), self.published_comment.content)
        self.assertEqual(comment.get('content'), self.published_comment.content)

    def test_all_comments_are_displayed(self):
        self.assertEqual(self.page.count_comments(), 10)

    def test_empty_comments_message(self):
        self.published_post.comments.all().delete()
        self.page.reload()

        self.assertTrue(self.page.is_empty_message_visible())

    def test_post_content_is_not_truncated(self):
        post_element = self.page.get_post_details()

        self.assertEqual(
            len(self.published_post.content), len(post_element.get('content')))

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
        self.assertEqual(num_comments, self.published_comments.count())
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

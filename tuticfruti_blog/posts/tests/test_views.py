# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from django.core.urlresolvers import reverse
from django import test

from .. import views
from .. import factories
from tuticfruti_blog.core import settings
from tuticfruti_blog.users.factories import UserFactory


class PostListViewTest(test.TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(
            author=self.user,
            status_id=settings.POST_PUBLIC_STATUS,
            content=settings.FUZZY_TEXTS[5])
        self.res = self.client.get(reverse('home'))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostListView.as_view().__name__)

    def test_post_variable_is_available_in_context_data(self):
        self.assertIn('posts', self.res.context_data)
        self.assertEqual(len(self.res.context_data['posts']), 1)

    def test_post_text_content_limit_variable_is_available_in_context_data(self):
        self.assertIn('post_text_content_limit', self.res.context_data)
        self.assertIn('post_text_content_limit', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_get_context_data_method(self):
        self.assertEqual(
            self.res.context_data.get('post_text_content_limit'),
            settings.POST_TEXT_CONTENT_LIMIT)

    def test_posts_num_comments_annotation(self):
        post = factories.PostFactory(author=self.user, title='test_posts_num_comments_annotation')
        factories.CommentFactory.create_batch(5, post=post)
        res = self.client.get(reverse('home'))

        for post in res.context_data.get('posts'):
            if post.title == 'test_posts_num_comments_annotation':
                self.assertEqual(post.num_comments, 5)

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test_get_queryset_method(self, mock_models):
        views.PostListView.get_queryset(mock.Mock(
            spec=views.PostListView,
            kwargs=dict(),
            request=mock.Mock(GET=dict())))
        self.assertTrue(mock_models.Post.objects.annotate.called)
        self.assertIsNone(mock_models.Post.objects.annotate().filter.assert_called_once_with(status_id=settings.POST_PUBLIC_STATUS))

    #
    #   Integrated tests
    #

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=settings.POST_DRAFT_STATUS)

        res = self.client.get(reverse('home'))
        self.assertNotContains(res, post.title)

    def test_order_by_created_date(self):
        factories.PostFactory.create_batch(10, author=self.user, status_id=settings.POST_PUBLIC_STATUS)

        res = self.client.get(reverse('home'))
        posts = res.context_data.get('posts')
        prev_post = None

        for current_post in posts:
            if prev_post:
                self.assertGreaterEqual(prev_post.created, current_post.created)
                prev_post = current_post
            else:
                prev_post = current_post


class PostListByCategoryViewTest(test.TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.res = self.client.get(
            reverse('posts:list_by_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)))

    #
    #   Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostListByCategoryView.as_view().__name__)

    def test_current_category_id_variable_is_available_in_context_data(self):
        self.assertIsNotNone(self.res.context_data.get('current_category_id'))
        self.assertEqual(self.res.context_data.get('current_category_id'), settings.PYTHON_CATEGORY)

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    @mock.patch('tuticfruti_blog.posts.views.PostListView.get_queryset')
    def test_get_queryset_method(self, mock_parent_get_queryset):
        mock_parent_get_queryset.return_value = mock.Mock(
            filter=mock.Mock(return_value=mock.sentinel.queryset))

        # Without category
        return_value = views.PostListByCategoryView.get_queryset(mock.Mock(
            spec=views.PostListByCategoryView,
            kwargs=dict(),
            request=mock.Mock(GET=dict())))

        self.assertEqual(return_value, mock_parent_get_queryset.return_value)

        # With category
        return_value = views.PostListByCategoryView.get_queryset(mock.Mock(
            spec=views.PostListByCategoryView,
            kwargs=dict(category_id=settings.PYTHON_CATEGORY),
            request=mock.Mock(GET=dict())))

        self.assertEqual(return_value, mock.sentinel.queryset)
        self.assertIsNone(mock_parent_get_queryset().filter.assert_called_once_with(
            category_id=settings.PYTHON_CATEGORY))

    #
    # Integrated tests
    #

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=settings.POST_DRAFT_STATUS)

        res = self.client.get(reverse('home', kwargs=dict()))
        self.assertNotContains(res, post.title)

        res = self.client.get(reverse('posts:list', kwargs=dict()))
        self.assertNotContains(res, post.title)

        res = self.client.get(reverse('posts:list_by_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)))
        self.assertNotContains(res, post.title)


class PostListSearchViewTest(test.TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.terms = [settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY]
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms='{} {}'.format(*self.terms)))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(
            self.res.resolver_match.func.__name__,
            views.PostListSearchView.as_view().__name__
        )

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_search_terms_variable_is_available_in_context_data(self):
        self.assertIsNotNone(self.res.context_data.get('search_terms'))
        self.assertEqual(self.res.context_data.get('search_terms'), '{} {}'.format(*self.terms))

    @mock.patch('tuticfruti_blog.posts.views.PostListByCategoryView.get_queryset')
    def test_get_queryset_method(self, mock_parent_get_queryset):
        mock_parent_get_queryset.return_value = mock.Mock(filter=mock.Mock(
            return_value=mock.Mock(distinct=mock.Mock(
                return_value=mock.sentinel.queryset))))

        return_value = views.PostListSearchView.get_queryset(mock.Mock(
            spec=views.PostListSearchView,
            kwargs=dict(),
            request=mock.Mock(GET=dict(search_terms='{} {}'.format(*self.terms)))))

        self.assertEqual(return_value, mock.sentinel.queryset)
        self.assertIsNone(mock_parent_get_queryset().filter.assert_called_once_with(
            tags__term__in=self.terms))

    #
    # Integrated tests
    #

    def test_distinct_search_result(self):
        tag1 = factories.TagFactory()
        tag2 = factories.TagFactory()
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)
        post.tags.add(tag1, tag2)
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='{} {}'.format(tag1.term, tag2.term)))

        self.assertEqual(len(res.context_data['posts']), 1)

    def test_search_category_filter_by_category(self):
        python_post = factories.PostFactory(
            author=self.user,
            category_id=settings.PYTHON_CATEGORY,
            status_id=settings.POST_PUBLIC_STATUS)
        django_post = factories.PostFactory(
            author=self.user,
            category_id=settings.DJANGO_CATEGORY,
            status_id=settings.POST_PUBLIC_STATUS)
        tag = factories.TagFactory()
        python_post.tags.add(tag)
        django_post.tags.add(tag)
        res = self.client.get(
            reverse('posts:search_by_category', kwargs=dict(category_id=settings.PYTHON_CATEGORY)),
            dict(search_terms=tag.term))

        self.assertEqual(len(res.context_data['posts']), 1)


class PostDetailViewTest(test.TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)
        self.res = self.client.get(reverse('posts:detail', kwargs=dict(slug=self.post.slug)))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostDetailView.as_view().__name__)

    def test_post_variable_is_available_in_context_data(self):
        self.assertIn('comments', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/detail.html', self.res.template_name)

    def test_comment_form_is_valid(self):
        self.fail('test_comment_form_is_valid FAULT')

    #
    # Integrated tests
    #

    def test_create_new_comment(self):
        self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)),
            dict(author='user0', email='user0@example.com', content=settings.FUZZY_TEXTS[0]))

        self.assertEqual(self.post.comment_set.count(), 1)

    def test_coments_order_by_created_date(self):
        comments = factories.CommentFactory.create_batch(10, post=self.post)
        self.post.comment_set.add(*comments)
        res = self.client.get(reverse('posts:detail', kwargs=dict(slug=self.post.slug)))

        prev_comment = None
        for comment in res.context_data['comments']:
            if prev_comment:
                self.assertGreaterEqual(prev_comment.created, comment.created)
                prev_comment = comment
            else:
                prev_comment = comment

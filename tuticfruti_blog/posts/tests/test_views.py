# -*- coding: utf-8 -*-
import unittest
from unittest import mock

from django.core.urlresolvers import reverse
from django import test

from .. import models
from .. import views
from .. import factories
from .. import forms
from tuticfruti_blog.core import settings
from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.users.factories import UserFactory


class PostListViewTest(test.TransactionTestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = factories.PostFactory(
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED,
            content=data_fixtures.FUZZY_TEXTS[5])
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

    def test_template_name(self):
        self.assertIn('posts/list.html', self.res.template_name)

    def test_get_context_data_method(self):
        self.assertEqual(
            self.res.context_data.get('post_text_content_limit'),
            models.Post.TEXT_CONTENT_LIMIT)

    def test_posts_comments__count_annotation(self):
        post = factories.PostFactory(author=self.user, title='test_posts_comments__count_annotation')
        factories.CommentFactory.create_batch(
            5, post=post, status_id=models.Comment.STATUS_PUBLISHED)
        res = self.client.get(reverse('home'))

        for post in res.context_data.get('posts'):
            if post.title == 'test_posts_comments__count_annotation':
                self.assertEqual(post.comments__count, 5)

    @mock.patch('tuticfruti_blog.posts.views.models')
    def test_get_queryset_method(self, mock_models):
        mock_request = mock.Mock(GET=dict())
        views.PostListView.get_queryset(mock.Mock(
            spec=views.PostListView,
            kwargs=dict(),
            request=mock_request))
        self.assertTrue(mock_models.Post.objects.annotate.called)
        self.assertIsNone(mock_models.Post.objects.annotate().filter.assert_called_once_with(
            status_id=mock_models.Post.STATUS_PUBLISHED))

    #
    #   Integrated tests
    #

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(
            author=self.user,
            title='Draft posts should not be displayed.',
            status_id=models.Post.STATUS_DRAFT)

        res = self.client.get(reverse('home'))
        self.assertNotContains(res, post.title)

    def test_order_by_created_date(self):
        factories.PostFactory.create_batch(
            10, author=self.user, status_id=models.Post.STATUS_PUBLISHED)

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
        mock_request = mock.Mock(GET=dict())
        mock_parent_get_queryset.return_value = mock.Mock(
            filter=mock.Mock(return_value=mock.sentinel.queryset))

        # Without category
        mock_post_list_by_category_view = mock.Mock(
            spec=views.PostListByCategoryView,
            kwargs=dict(),
            request=mock_request)

        return_value = views.PostListByCategoryView.get_queryset(mock_post_list_by_category_view)

        self.assertEqual(return_value, mock_parent_get_queryset.return_value)

        # With category
        mock_post_list_by_category_view = mock.Mock(
            spec=views.PostListByCategoryView,
            kwargs=dict(category_id=settings.PYTHON_CATEGORY),
            request=mock_request)

        return_value = views.PostListByCategoryView.get_queryset(mock_post_list_by_category_view)

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
            status_id=models.Post.STATUS_DRAFT)

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
        mock_request = mock.Mock(GET=dict(search_terms='{} {}'.format(*self.terms)))
        mock_parent_get_queryset.return_value.filter.return_value.distinct.return_value = mock.sentinel.queryset
        mock_post_list_search_view = mock.Mock(
            spec=views.PostListSearchView,
            kwargs=dict(),
            request=mock_request)

        return_value = views.PostListSearchView.get_queryset(mock_post_list_search_view)

        self.assertEqual(return_value, mock.sentinel.queryset)
        self.assertIsNone(mock_parent_get_queryset().filter.assert_called_once_with(
            tags__term__in=self.terms))

    #
    # Integrated tests
    #

    def test_distinct_search_result(self):
        tag1 = factories.TagFactory()
        tag2 = factories.TagFactory()
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        post.tags.add(tag1, tag2)
        res = self.client.get(
            reverse('posts:search', kwargs=dict()),
            dict(search_terms='{} {}'.format(tag1.term, tag2.term)))

        self.assertEqual(len(res.context_data['posts']), 1)

    def test_search_category_filter_by_category(self):
        python_post = factories.PostFactory(
            author=self.user,
            category_id=settings.PYTHON_CATEGORY,
            status_id=models.Post.STATUS_PUBLISHED)
        django_post = factories.PostFactory(
            author=self.user,
            category_id=settings.DJANGO_CATEGORY,
            status_id=models.Post.STATUS_PUBLISHED)
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
        self.post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        self.res = self.client.get(reverse('posts:detail', kwargs=dict(slug=self.post.slug)))

    #
    # Unit tests
    #

    def test_http_request_ok(self):
        self.assertEqual(self.res.status_code, 200)

    def test_url_conf_resolver(self):
        self.assertEqual(self.res.resolver_match.func.__name__, views.PostDetailView.as_view().__name__)

    def test_post_variable_is_available_in_context_data(self):
        self.assertIn('post', self.res.context_data)

    def test_comments_variable_is_available_in_context_data(self):
        self.assertIn('comments', self.res.context_data)

    def test_form_variable_is_available_in_context_data(self):
        self.assertIn('form', self.res.context_data)

    def test_template_name(self):
        self.assertIn('posts/detail.html', self.res.template_name)

    def test_comment_form_author_validation(self):
        comment_form = forms.CommentForm(dict(author='user0'))
        self.assertFalse(comment_form['author'].errors)

        comment_form = forms.CommentForm(dict(author=''))
        self.assertTrue(comment_form['author'].errors)

    def test_comment_form_email_validation(self):
        comment_form = forms.CommentForm(dict(email='user0@example.com'))
        self.assertFalse(comment_form['email'].errors)

        comment_form = forms.CommentForm(dict(email=''))
        self.assertTrue(comment_form['email'].errors)

        comment_form = forms.CommentForm(dict(email='user0'))
        self.assertTrue(comment_form['email'].errors)

    def test_comment_form_content_validation(self):
        comment_form = forms.CommentForm(dict(content='Content ...'))
        self.assertFalse(comment_form['content'].errors)

        comment_form = forms.CommentForm(dict(content=''))
        self.assertTrue(comment_form['content'].errors)

    @mock.patch('tuticfruti_blog.posts.views.generic_views.DetailView.get_context_data')
    def test_get_context_data_method(self, mock_parent_get_context_data):
        mock_parent_get_context_data.return_value = dict()
        mock_get_form = mock.Mock(return_value=mock.sentinel.context_form)
        mock_get_object = mock.Mock()
        mock_get_object.return_value.comments.filter.return_value.order_by.return_value = mock.sentinel.context_comments
        mock_post_detail_post = mock.Mock(
            spec=views.PostDetailView,
            get_form=mock_get_form,
            get_object=mock_get_object)

        context = views.PostDetailView.get_context_data(mock_post_detail_post)

        self.assertEqual(context['form'], mock.sentinel.context_form)
        self.assertEqual(context['comments'], mock.sentinel.context_comments)
        self.assertIsNone(mock_get_object().comments.filter.assert_called_once_with(
            status_id=models.Comment.STATUS_PUBLISHED))
        self.assertIsNone(mock_get_object().comments.filter().order_by.assert_called_once_with(
            models.Post.ORDERING))

    def test_post_method(self):
        # Valid form
        mock_get_form = mock.Mock()
        mock_get_form.return_value.is_valid.return_value = True
        mock_form_valid = mock.Mock(return_value=mock.sentinel.form_valid)
        mock_form_invalid = mock.Mock(return_value=mock.sentinel.form_invalid)
        mock_request = mock.Mock()
        mock_post_detail_view = mock.Mock(
            spec=views.PostDetailView,
            get_form=mock_get_form,
            form_valid=mock_form_valid,
            form_invalid=mock_form_invalid)

        return_value = views.PostDetailView.post(mock_post_detail_view, mock_request)

        self.assertEqual(return_value, mock.sentinel.form_valid)

        # Invalid form
        mock_get_form.return_value.is_valid.return_value = False
        mock_post_detail_view = mock.Mock(
            spec=views.PostDetailView,
            get_form=mock_get_form,
            form_valid=mock_form_valid,
            form_invalid=mock_form_invalid)

        return_value = views.PostDetailView.post(mock_post_detail_view, mock_request)

        self.assertEqual(return_value, mock.sentinel.form_invalid)

    @mock.patch('tuticfruti_blog.posts.views.models.Comment.objects.create')
    def test_form_valid_method(self, mock_create):
        mock_get_object = mock.Mock(return_value=mock.sentinel.post)
        form = forms.CommentForm(dict(
            author=mock.sentinel.author,
            email=mock.sentinel.email,
            content=mock.sentinel.content))
        mock_post_detail_view = mock.Mock(
            spec=views.PostDetailView,
            get_object=mock_get_object)

        views.PostDetailView.form_valid(mock_post_detail_view, form)

        self.assertIsNone(mock_create.assert_called_once_with(
            post=mock.sentinel.post,
            author=mock.sentinel.author,
            email=mock.sentinel.email,
            content=mock.sentinel.content))

    #
    # Integrated tests
    #

    def test_create_new_comment(self):
        self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.post.slug)),
            dict(author='user0', email='user0@example.com', content=data_fixtures.FUZZY_TEXTS[0]))

        self.assertEqual(self.post.comments.count(), 1)

    def test_coments_order_by_created_date(self):
        comments = factories.CommentFactory.create_batch(10, post=self.post)
        self.post.comments.add(*comments)
        res = self.client.get(reverse('posts:detail', kwargs=dict(slug=self.post.slug)))

        prev_comment = None
        for comment in res.context_data['comments']:
            if prev_comment:
                self.assertGreaterEqual(prev_comment.created, comment.created)
                prev_comment = comment
            else:
                prev_comment = comment

    def test_only_public_comments_are_displayed(self):
        self.fail('test_only_public_comments_are_displayed FAULT')

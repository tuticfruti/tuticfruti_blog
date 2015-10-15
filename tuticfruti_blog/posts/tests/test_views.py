# -*- coding: utf-8 -*-
import unittest

from django.core.urlresolvers import reverse
from django import test

from .. import models
from .. import views
from .. import factories
from tuticfruti_blog.core import data_fixtures


class TestViewCommonMixin:
    view = None
    context_data_vars = None
    template_name = None

    def test_http_request_ok(self):
        status_code_expected = 200
        status_code = self.res.status_code

        self.assertEqual(status_code, status_code_expected)

    def test_url_conf_resolver(self):
        if self.view is None:
            self.fail('Variable class "view" was not defined in {} class'.format(
                self.__class__.__name__))
        func_name_expected = self.view.as_view().__name__
        func_name = self.res.resolver_match.func.__name__

        self.assertEqual(func_name, func_name_expected)

    def test_posts_variable_is_available_in_context_data(self):
        if self.context_data_vars is None:
            self.fail('Variable class "context_data_vars" was not defined in {} class'.format(
                self.__class__.__name__))
        context_data = self.res.context_data

        for key_expected in self.context_data_vars:
            self.assertIn(key_expected, context_data)

    def test_template_name(self):
        if self.template_name is None:
            self.fail('Variable class "template_name" was not defined in {} class'.format(
                self.__class__.__name__))
        template_expected = self.template_name
        template = self.res.template_name

        self.assertIn(template_expected, template)


class TestViewBase(test.TestCase):
    @classmethod
    def setUpClass(cls):
        if cls is TestViewBase:
            raise unittest.SkipTest('Skip base class tests')
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        data_fixtures.DataFixtures.load()

        # Posts
        cls.published_posts = models.Post.objects \
            .filter(status_id=models.Post.STATUS_PUBLISHED) \
            .order_by(*models.Post._meta.ordering)
        cls.published_post = models.Post.objects.get(slug='published-post')
        cls.draft_post = models.Post.objects.get(slug='draft-post')

        # Categories
        cls.enabled_post_categories = cls.published_post.categories \
            .filter(is_enabled=True) \
            .order_by(*models.Category._meta.ordering)
        cls.enabled_categories = models.Category.objects \
            .filter(is_enabled=True) \
            .order_by(*models.Category._meta.ordering)
        cls.python_category = models.Category.objects.get(slug='python')
        cls.first_category = models.Category.objects.get(slug='first-category')
        cls.disabled_category = models.Category.objects.get(slug='disabled-category')

        # Tags
        cls.tags = models.Tag.objects.all().order_by(*models.Tag._meta.ordering)
        cls.python_tag = models.Tag.objects.get(term='python')
        cls.django_tag = models.Tag.objects.get(term='django')
        cls.miscellaneous_tag = models.Tag.objects.get(term='miscellaneous')

        # Comments
        cls.published_post_comments = cls.published_post.comments \
            .filter(status_id=models.Comment.STATUS_PUBLISHED) \
            .order_by(*models.Comment._meta.ordering)
        cls.pending_post_comments = cls.published_post.comments \
            .filter(status_id=models.Comment.STATUS_PENDING)


class TestPostListView(TestViewCommonMixin, TestViewBase):
    view = views.PostListView
    context_data_vars = ['posts', 'categories']
    template_name = 'posts/list.html'

    def setUp(self):
        self.res = self.client.get(reverse('home'))

    def test_only_public_posts_are_displayed(self):
        post_not_expected = self.draft_post
        posts = self.res.context_data.get('posts')

        self.assertNotIn(post_not_expected, posts)

    def test_all_categories_are_sorted_and_enabled(self):
        categories_expected = self.enabled_categories
        categories = self.res.context_data.get('categories')

        for i in range(len(categories)):
            self.assertEqual(categories[i], categories_expected[i])

    def test_all_post_categories_are_sorted_and_enabled(self):
        categories_expected = self.enabled_post_categories
        posts = self.res.context_data.get('posts')
        for post in posts:
            if post.slug == 'published-post':
                break
        categories = post.categories.all()

        for i in range(len(categories)):
            self.assertTrue(categories[i].is_enabled)
        for i in range(len(categories)):
            self.assertEqual(categories[i], categories_expected[i])


class TestPostListByCategoryView(TestViewCommonMixin, TestViewBase):
    view = views.PostListByCategoryView
    context_data_vars = ['current_category']
    template_name = 'posts/list.html'

    def setUp(self):
        self.res = self.client.get(reverse(
            'posts:list_by_category',
            kwargs=dict(slug=self.python_category.slug)))

    def test_filter_posts_by_python_category(self):
        posts_expected = self.published_posts.filter(categories__in=[self.python_category])
        posts = self.res.context_data.get('posts')

        for i in range(len(posts)):
            self.assertEqual(posts[i], posts_expected[i])


class TestPostListSearchView(TestViewCommonMixin, TestViewBase):
    view = views.PostListSearchView
    context_data_vars = ['search_terms']
    template_name = 'posts/list.html'

    def setUp(self):
        self.res = self.client.get(
            reverse('posts:search'),
            dict(search_terms='python'))

    def test_search_is_case_insensitive(self):
        posts_expected = self.published_posts.filter(tags__in=[self.python_tag])
        self.res = self.client.get(reverse('posts:search'), dict(search_terms='PYTHON'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())

    def test_result_has_no_repeated(self):
        posts_expected = self.published_posts.filter(tags__in=[self.python_tag]).distinct()
        self.res = self.client.get(reverse('posts:search'), dict(search_terms='python python'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())

    def test_restrict_result_by_category(self):
        posts_expected = models.Post.objects \
            .filter(categories__in=[self.python_category]) \
            .filter(tags__in=[self.python_tag, self.django_tag, self.miscellaneous_tag]) \
            .distinct()
        self.res = self.client.get(
            reverse(
                'posts:search_by_category',
                kwargs=dict(slug=self.python_category.slug)),
            dict(search_terms='python django miscellaneous'))
        posts = self.res.context_data.get('posts')

        self.assertEqual(posts.count(), posts_expected.count())

    def test_search_is_case_unsensitive(self):
        num_posts_expected = self.published_posts \
            .filter(tags__term__iregex=r'(python)') \
            .count()
        res = self.client.get(reverse('posts:search'), dict(search_terms='PYTHON'))
        num_posts = res.context_data.get('posts').count()

        self.assertEqual(num_posts, num_posts_expected)

    def test_search_consider_also_category_field(self):
        num_posts_expected = self.published_posts \
            .filter(categories__name__iregex=r'(first)') \
            .count()
        res = self.client.get(reverse('posts:search'), dict(search_terms='first'))
        num_posts = res.context_data.get('posts').count()

        self.assertEqual(num_posts, num_posts_expected)

    def test_search_consider_also_title_field(self):
        num_posts_expected = self.published_posts \
            .filter(title__iregex=r'(published)') \
            .count()
        res = self.client.get(reverse('posts:search'), dict(search_terms='published'))
        num_posts = res.context_data.get('posts').count()

        self.assertEqual(num_posts, num_posts_expected)


class TestPostDetailView(TestViewCommonMixin, TestViewBase):
    view = views.PostDetailView
    context_data_vars = ['post', 'form', 'categories']
    template_name = 'posts/detail.html'

    def setUp(self):
        self.res = self.client.get(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)))

    def test_send_a_valid_form_comment(self):
        num_comments_expected = self.pending_post_comments.count()
        res = self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            dict(
                author='anonymous',
                email='anonymous@example.com',
                content=factories.FUZZY_TEXTS[0]),
            follow=True)
        num_comments = self.pending_post_comments.count()

        self.assertEqual(num_comments, num_comments_expected + 1)
        self.assertIn(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            res.redirect_chain[0][0])

    def test_send_an_invalid_form_comment(self):
        num_comments_expected = self.pending_post_comments.count()
        self.client.post(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            dict(
                author=None,
                email=None,
                content=None))
        num_comments = self.pending_post_comments.count()

        self.assertEqual(num_comments, num_comments_expected)

    def test_comments_are_sorted_by_created_field(self):
        comments_expected = self.published_post_comments
        comments = self.res.context_data.get('post').comments.all()

        for i in range(len(comments)):
            self.assertEqual(comments[i], comments_expected[i])

    def test_all_post_tags_are_sorted_by_alphabetical_order(self):
        tags_expected = self.tags
        tags = self.res.context_data.get('post').tags.all()

        for i in range(len(tags)):
            self.assertEqual(tags[i], tags_expected[i])

    def test_all_categories_are_sorted_and_enabled(self):
        categories_expected = self.enabled_categories
        categories = self.res.context_data.get('post').categories.all()

        for i in range(len(categories)):
            self.assertEqual(categories[i], categories_expected[i])

    def test_only_published_comments_are_counted(self):
        comments_expected = self.published_post_comments
        comments = self.res.context_data.get('post').comments.all()

        self.assertEqual(comments.count(), comments_expected.count())

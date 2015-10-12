# -*- coding: utf-8 -*-
import datetime
import re

from django.core.urlresolvers import reverse

from . import functional_test
from .pom import pages

from tuticfruti_blog.posts import factories
from tuticfruti_blog.posts import models


class TestHomePage(functional_test.FunctionalTest):
    @property
    def _num_pages(self):
        num_posts = models.Post.objects.all_published().count()
        if num_posts % models.Post.PAGINATE_BY:
            num_pages = int(num_posts / models.Post.PAGINATE_BY) + 1
        else:
            num_pages = int(num_posts / models.Post.PAGINATE_BY)
        return num_pages

    def setUp(self):
        super().setUpTestData()
        self.page = pages.HomePage(self.live_server_url)
        self.page.open()

    def tearDown(self):
        self.page.close()

    def test_home_page_link(self):
        url_expected = self.page.url
        self.page.goto_home_page()
        current_url = self.page.current_driver_url

        self.assertEqual(current_url, url_expected)

    def test_read_more_link(self):
        url_expected = reverse('posts:detail', kwargs=dict(slug=self.published_post.slug))
        self.page.click_on_read_me_link(self.published_post.pk)
        current_url = self.page.current_driver_url

        self.assertIn(url_expected, current_url)

    def test_empty_message(self):
        models.Post.objects.all().delete()
        self.page.reload()
        self.assertTrue(self.page.is_empty_message_visible())

    def test_max_number_of_posts_per_page(self):
        num_posts_expected = models.Post.PAGINATE_BY
        for i in range(self._num_pages - 1):
            num_posts = self.page.count_posts()

        self.assertLessEqual(num_posts, num_posts_expected)

    def test_posts_chronological_order(self):
        post_expected = factories.PostFactory(
            author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        self.page.reload()
        post = self.page.get_post_details_by_key(0)

        self.assertEqual(post.get('pk'), post_expected.pk)

    def test_prev_next_pagination_buttons(self):
        # Prev page link is not visible
        self.assertFalse(self.page.is_prev_link_visible())

        # Go to last page
        for i in range(self._num_pages - 1):
            self.page.goto_next_page()

        self.assertFalse(self.page.is_next_link_visible())
        self.assertTrue(self.page.is_prev_link_visible())
        self.assertEqual(self.page.current_page, self._num_pages)

        # Go to first page
        for i in range(self._num_pages - 1):
            self.page.goto_prev_page()

        self.assertTrue(self.page.is_next_link_visible())
        self.assertFalse(self.page.is_prev_link_visible())
        self.assertEqual(self.page.current_page, 1)

    def test_search_terms_with_and_without_category_selected(self):
        # User searchs "python" and "django" terms without category selected
        terms = '{} {}'.format(
            self.python_category.name, self.django_category.name)
        posts_expected = self.published_posts \
            .filter(tags__in=[self.python_tag, self.django_tag]) \
            .distinct()
        self.page.search_posts(terms)

        self.assertEqual(self.page.count_posts(), posts_expected.count())

        # User searchs "python" and "django" with Python category selected
        posts_expected = self.published_posts \
            .filter(categories__in=[self.python_category]) \
            .filter(tags__in=[self.python_tag, self.django_tag]) \
            .distinct()
        self.page.search_posts(terms, self.python_category.pk)

        self.assertEqual(self.page.count_posts(), posts_expected.count())

        # User searchs "python" and "django" terms with Django category selected
        posts_expected = self.published_posts \
            .filter(categories__in=[self.django_category]) \
            .filter(tags__in=[self.python_tag, self.django_tag]) \
            .distinct()
        self.page.search_posts(terms, self.django_category.pk)

        self.assertEqual(self.page.count_posts(), posts_expected.count())

        # User searchs "python" and "miscellaneous" terms with Miscellaneous category selected
        terms = '{} {}'.format(
            self.python_category.name, self.miscellaneous_category.name)
        posts_expected = self.published_posts \
            .filter(categories__in=[self.miscellaneous_category]) \
            .filter(tags__in=[self.python_tag, self.django_tag, self.miscellaneous_tag]) \
            .distinct()
        self.page.search_posts(terms, self.miscellaneous_category.pk)

        self.assertEqual(self.page.count_posts(), posts_expected.count())

    def test_only_published_comments_are_counted(self):
        post = self.page.get_post_details_by_pk(self.published_post.pk)

        self.assertEqual(
            post.get('num_comments'), str(self.published_post_comments.count()))

    def test_comments_link(self):
        url_expected = '{}{}'.format(
            reverse('posts:detail', kwargs=dict(slug=self.published_post.slug)),
            '#comments_id')
        self.page.click_on_num_comments_link(self.published_post.pk)
        current_url = self.page.current_driver_url

        self.assertIn(url_expected, current_url)

    def test_only_public_posts_are_displayed(self):
        posts_expected = models.Post.objects.all_published()
        num_posts = self.page.count_posts()
        for i in range(self._num_pages - 1):
            self.page.goto_next_page()
            num_posts += self.page.count_posts()

        self.assertEqual(num_posts, posts_expected.count())

    def test_enabled_categories_are_displayed(self):
        num_categories = self.page.count_categories()

        self.assertEqual(num_categories, self.enabled_categories.count())

    def test_categories_are_sorted_by_order_field(self):
        for i in range(self.enabled_categories.count()):
            category = self.page.get_category_details_by_key(i)
            self.assertEqual(category.get('pk'), self.enabled_categories[i].pk)

    def test_filter_by_category(self):
        posts_expected = self.published_posts \
            .filter(categories__in=[self.python_category])
        self.page.select_category(self.python_category.pk)
        num_posts = self.page.count_posts()

        self.assertEqual(num_posts, posts_expected.count())

    def test_current_active_category(self):
        # Firs time, all categories are inactive
        for category in self.enabled_categories:
            self.assertFalse(self.page.is_category_enabled(category.pk))

        # Current category is category selected
        for category in self.enabled_categories:
            self.page.select_category(category.pk)
            self.assertTrue(self.page.is_category_enabled(category.pk))

    def test_disabled_link_to_comments_if_no_comments_found(self):
        url_expected = self.page.current_driver_url
        self.page.click_on_num_comments_link(self.post_without_comments.pk)
        current_url = self.page.current_driver_url

        self.assertEqual(current_url, url_expected)

    def test_post_detail(self):
        categories_expected = self.published_post.categories.all_enabled().values_list('name', flat=True)
        tags_expected = self.published_post.tags.all().values_list('term', flat=True)
        post_expected = self.published_post

        search_result = re.search(models.Post.HR, post_expected.content)
        if search_result:
            content_expected = post_expected.content[:search_result.start()]
        else:
            content_expected = post_expected.content

        comments_expected = self.published_post_comments
        date_expected = '{dt:%B} {dt.day}, {dt.year}'.format(dt=post_expected.created)
        post = self.page.get_post_details_by_pk(post_expected.pk)

        self.assertEqual(post.get('id'), post_expected.id)
        self.assertEqual(post.get('pk'), post_expected.pk)
        self.assertEqual(post.get('author'), post_expected.author.username)
        self.assertEqual(post.get('title'), post_expected.title)
        self.assertEqual(post.get('num_comments'), str(comments_expected.count()))
        self.assertEqual(post.get('created'), date_expected)
        self.assertEqual(post.get('tags'), ' '.join(tags_expected))
        self.assertEqual(post.get('categories'), ' '.join(categories_expected))
        self.assertHTMLEqual(post.get('content'), content_expected)

    def test_post_content_is_hr_truncated(self):
        search_result = re.search(models.Post.HR, self.published_post.content)
        if search_result:
            content_expected = self.published_post.content[:search_result.start()].strip()
        else:
            self.fail('published_post.content field must contain {} string'.format(models.Post.HR))
        post = self.page.get_post_details_by_pk(self.published_post.pk)
        content = post.get('content')

        self.assertEqual(content, content_expected)

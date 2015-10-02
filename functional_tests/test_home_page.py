# -*- coding: utf-8 -*-
import datetime

from selenium.common.exceptions import NoSuchElementException

from django.core.urlresolvers import reverse
from django.utils import timezone

from . import functional_test
from .pom import pages

from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.posts import factories
from tuticfruti_blog.posts import models


class TestHomePage(functional_test.FunctionalTest):
    def setUp(self):
        super().setUpTestData()
        self.page = pages.HomePage(self.live_server_url)
        self.page.open()

    def tearDown(self):
        self.page.close()

    def test_home_page_link(self):
        self.page.goto_home_page()
        self.assertEqual(self.page.url, self.page.current_driver_url)

    def test_read_more_link(self):
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)

        self.page.reload()
        self.page.click_on_read_me_link(post.pk)

        self.assertEqual(
            self.page.current_driver_url,
            '{}{}'.format(self.live_server_url, reverse('posts:detail', kwargs=dict(slug=post.slug))))

    def test_empty_message(self):
        self.assertTrue(self.page.is_empty_message_visible())

    def test_orphans_posts(self):
        factories.PostFactory.create_batch(
            models.Post.PAGINATE_BY + 1,
            status_id=models.Post.STATUS_PUBLISHED,
            author=self.user)
        self.page.reload()

        self.assertEqual(self.page.count_posts(), models.Post.PAGINATE_BY + 1)

    def test_max_number_of_posts_per_page(self):
        factories.PostFactory.create_batch(
            models.Post.PAGINATE_BY + 2,
            status_id=models.Post.STATUS_PUBLISHED,
            author=self.user)
        self.page.reload()

        self.assertEqual(self.page.count_posts(), models.Post.PAGINATE_BY)

    def test_posts_chronological_order(self):
        post = factories.PostFactory(status_id=models.Post.STATUS_PUBLISHED, author=self.user)
        another_post = factories.PostFactory(status_id=models.Post.STATUS_PUBLISHED, author=self.user)

        # Post created in January month
        post.created = datetime.datetime(2015, 1, 1, tzinfo=timezone.get_current_timezone())
        post.save()

        # Post created in February month
        another_post.created = datetime.datetime(2015, 2, 1, tzinfo=timezone.get_current_timezone())
        another_post.save()
        self.page.reload()

        self.assertTrue('February' in self.page.get_post_details_by_key(0).get('created'))

    def test_prev_next_pagination_buttons(self):
        factories.PostFactory.create_batch(
            3*models.Post.PAGINATE_BY,
            status_id=models.Post.STATUS_PUBLISHED,
            author=self.user)
        self.page.reload()

        # Prev page link is not visible
        self.assertFalse(self.page.is_prev_link_visible())

        # User go to Next page twice
        self.page.goto_next_page()
        self.page.goto_next_page()
        self.assertEqual(self.page.current_page, 3)

        # Next page link is not visible
        self.assertFalse(self.page.is_next_link_visible())

        # User come back to home page
        self.page.goto_prev_page()
        self.page.goto_prev_page()
        self.assertEqual(self.page.current_page, 1)

    def test_search_terms_with_and_without_category_selected(self):
        python_post = factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(self.python_category.name),
            status_id=models.Post.STATUS_PUBLISHED,
            tags=[factories.TagFactory.build(term=self.python_category.name)])
        python_post.categories.add(self.python_category)
        django_post = factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(self.django_category.name),
            status_id=models.Post.STATUS_PUBLISHED,
            tags=[factories.TagFactory.build(term=self.django_category.name)])
        django_post.categories.add(self.django_category)
        miscellaneous_post = factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(self.miscellaneous_category.name),
            status_id=models.Post.STATUS_PUBLISHED,
            tags=[factories.TagFactory.build(term=self.miscellaneous_category.name)])
        miscellaneous_post.categories.add(self.miscellaneous_category)
        self.page.reload()

        # User searchs "python" and "django" terms in All posts
        terms = '{} {}'.format(self.python_category.name, self.django_category.name)
        self.page.search_posts(terms)
        self.assertEqual(self.page.count_posts(), 2)

        # User searchs "python" and "django" terms in Python posts
        self.page.search_posts(terms, self.python_category.pk)
        self.assertEqual(self.page.count_posts(), 1)

        # User searchs "python" and "django" terms in Django posts
        self.page.search_posts(terms, self.django_category.pk)
        self.assertEqual(self.page.count_posts(), 1)

        # User searchs "python" and "miscellaneous" terms in Miscellaneous posts
        terms = '{} {}'.format(self.python_category.name, self.miscellaneous_category.name)
        self.page.search_posts(terms, self.miscellaneous_category.pk)
        self.assertEqual(self.page.count_posts(), 1)

    def test_only_published_comments_are_counted(self):
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        factories.CommentFactory(post=post, status_id=models.Comment.STATUS_PENDING)
        factories.CommentFactory(post=post, status_id=models.Comment.STATUS_PUBLISHED)
        self.page.reload()
        num_comments_element = self.page.get_post_details_by_pk(post.pk)

        self.assertEqual(num_comments_element.get('num_comments'), str(1))

    def test_post_details(self):
        post = factories.PostFactory(
            author=self.user,
            status_id=models.Post.STATUS_PUBLISHED,
            content=data_fixtures.FUZZY_TEXTS[5])
        post.tags.add(
            factories.TagFactory(term='term0'),
            factories.TagFactory(term='term1'))
        post.categories.add(
            factories.CategoryFactory(name='category1'),
            factories.CategoryFactory(name='category2'))
        factories.CommentFactory.create_batch(
            5, post=post, status_id=models.Comment.STATUS_PUBLISHED)

        self.page.reload()
        post_element = self.page.get_post_details_by_pk(post.pk)

        self.assertEqual(post_element.get('author'), post.author.username)
        self.assertEqual(post_element.get('title'), post.title)
        self.assertEqual(post_element.get('num_comments'), str(5))
        self.assertEqual(
            post_element.get('created'),
            '{dt:%B} {dt.day}, {dt.year}'.format(dt=post.created))
        self.assertEqual(post_element.get('tags'), 'term0 term1')
        self.assertEqual(post_element.get('categories'), 'category1 category2')
        self.assertHTMLEqual(
            post_element.get('content'),
            '{}{}'.format(post.content[:models.Post.TEXT_CONTENT_LIMIT-3], '...'))

    def test_post_content_must_be_truncated(self):
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)
        self.page.reload()
        post_element = self.page.get_post_details_by_pk(post.pk)
        self.assertLessEqual(len(post_element.get('content')), models.Post.TEXT_CONTENT_LIMIT)

    def test_comments_link(self):
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_PUBLISHED)

        self.page.reload()
        self.page.click_on_num_comments_link(post.pk)

        self.assertEqual(
            '{}{}{}'.format(
                self.live_server_url,
                reverse('posts:detail', kwargs=dict(slug=post.slug)),
                '#comments_id'),
            self.page.current_driver_url)

    def test_only_public_posts_are_displayed(self):
        post = factories.PostFactory(author=self.user, status_id=models.Post.STATUS_DRAFT)

        self.page.reload()

        with self.assertRaises(NoSuchElementException):
            self.page.get_post_details_by_pk(post.pk)

    def test_all_active_categories_are_displayed(self):
        categories = models.Category.objects.filter(is_active=True)

        for category in categories:
            self.assertTrue(self.page.is_category_displayed(category.pk))

    def test_only_active_categories_are_displayed(self):
        category = factories.CategoryFactory(name='Disabled category', is_active=False)
        self.page.reload()

        self.assertFalse(self.page.is_category_displayed(category.pk))

    def test_categories_asc_order(self):
        category = factories.CategoryFactory(name='First category', is_active=True, order=-1)
        self.page.reload()
        self.assertEqual(self.page.get_category_details_by_key(0).get('name'), category.name)

    def test_filter_by_category(self):
        categories = models.Category.objects.filter(is_active=True)
        for category in categories:
            post = factories.PostFactory(status_id=models.Post.STATUS_PUBLISHED)
            post.categories.add(category)
        self.page.reload()

        for category in categories:
            self.page.select_category(category.pk)
            post = self.page.get_post_details_by_key(0)
            self.assertEqual(self.page.count_posts(), 1)
            self.assertTrue(category.name in post.get('categories'))

    def test_current_active_category(self):
        categories = models.Category.objects.filter(is_active=True)
        # Firs time, all categories are disabled
        for category in categories:
            self.assertFalse(self.page.is_category_enabled(category.pk))

        # Current category is category selected
        for category in categories:
            self.page.select_category(category.pk)
            self.assertTrue(self.page.is_category_enabled(category.pk))

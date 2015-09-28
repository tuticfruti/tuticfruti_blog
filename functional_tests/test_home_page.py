# -*- coding: utf-8 -*-
import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone

from .pom import pages
from .base_page import FunctionalTest

from tuticfruti_blog.core import settings
from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.posts import factories


class HomePageTest(FunctionalTest):
    def setUp(self):
        self.user = UserFactory()
        self.home_page = pages.HomePage(self.live_server_url)
        self.home_page.open()

    def tearDown(self):
        self.home_page.close()

    def test_home_page_link(self):
        self.home_page.goto_home_page()
        self.assertEqual(self.home_page.url, self.home_page.current_driver_url)

    def test_read_more_link(self):
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)

        self.home_page.reload()
        self.home_page.click_on_read_me_link(post.pk)

        self.assertEqual(
            self.home_page.current_driver_url,
            '{}{}'.format(self.live_server_url, reverse('posts:detail', kwargs=dict(slug=post.slug))))

    def test_current_active_category(self):
        # Firs time, all categories are disabled
        self.assertFalse(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

        # User selects Python category
        self.home_page.select_category(settings.PYTHON_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))

        # User selects Django category
        self.home_page.select_category(settings.DJANGO_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))

        # User selects Miscellaneous category
        self.home_page.select_category(settings.MISCELLANEOUS_CATEGORY)
        self.assertTrue(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

        # User come back to Home page
        self.home_page.goto_home_page()
        self.assertFalse(self.home_page.is_category_enabled(settings.PYTHON_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.DJANGO_CATEGORY))
        self.assertFalse(self.home_page.is_category_enabled(settings.MISCELLANEOUS_CATEGORY))

    def test_filter_by_category_id(self):
        factories.PostFactory(
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.PYTHON_CATEGORY,
            author=self.user)
        factories.PostFactory(
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.DJANGO_CATEGORY,
            author=self.user)
        factories.PostFactory(
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.MISCELLANEOUS_CATEGORY,
            author=self.user)

        # User selects Python category
        self.home_page.select_category(settings.PYTHON_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User selects Django category
        self.home_page.select_category(settings.DJANGO_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User selects Miscellaneous category
        self.home_page.select_category(settings.MISCELLANEOUS_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User come back to Home page
        self.home_page.goto_home_page()
        self.assertEqual(self.home_page.count_posts(), 3)

    def test_empty_page(self):
        self.assertTrue(self.home_page.is_empty_message_visible())

    def test_orphans_posts(self):
        factories.PostFactory.create_batch(
            settings.PAGINATE_BY + 1,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)

        self.home_page.reload()

        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY + 1)

    def test_number_of_posts_limit(self):
        factories.PostFactory.create_batch(
            settings.PAGINATE_BY + 2,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)

        self.home_page.reload()

        self.assertEqual(self.home_page.count_posts(), settings.PAGINATE_BY)

    def test_posts_order(self):
        post = factories.PostFactory(status_id=settings.POST_PUBLIC_STATUS, author=self.user)
        another_post = factories.PostFactory(status_id=settings.POST_PUBLIC_STATUS, author=self.user)

        # Post created in January month
        post.created = datetime.datetime(2015, 1, 1, tzinfo=timezone.get_current_timezone())
        post.save()

        # Post created in February month
        another_post.created = datetime.datetime(2015, 2, 1, tzinfo=timezone.get_current_timezone())
        another_post.save()

        self.home_page.reload()

        self.assertTrue('February' in self.home_page.get_post_details_by_key(0).get('created'))

    def test_prev_next_buttons(self):
        factories.PostFactory.create_batch(
            3*settings.PAGINATE_BY,
            status_id=settings.POST_PUBLIC_STATUS,
            author=self.user)

        self.home_page.reload()

        # Prev page link is not visible
        self.assertFalse(self.home_page.is_prev_link_visible())

        # User go to Next page twice
        self.home_page.goto_next_page()
        self.home_page.goto_next_page()
        self.assertEqual(self.home_page.current_page, 3)

        # Next page link is not visible
        self.assertFalse(self.home_page.is_next_link_visible())

        # User come back to home page
        self.home_page.goto_prev_page()
        self.home_page.goto_prev_page()
        self.assertEqual(self.home_page.current_page, 1)

    def test_search_terms_with_and_without_category_selected(self):
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.PYTHON_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.PYTHON_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.PYTHON_CATEGORY)])
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.DJANGO_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.DJANGO_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.DJANGO_CATEGORY)])
        factories.PostFactory(
            author=self.user,
            title='Post title {}'.format(settings.MISCELLANEOUS_CATEGORY),
            status_id=settings.POST_PUBLIC_STATUS,
            category_id=settings.MISCELLANEOUS_CATEGORY,
            tags=[factories.TagFactory.build(term=settings.MISCELLANEOUS_CATEGORY)])

        self.home_page.reload()

        # User searchs on All posts
        terms = '{} {}'.format(settings.PYTHON_CATEGORY, settings.DJANGO_CATEGORY)
        self.home_page.search_posts(terms)
        self.assertEqual(self.home_page.count_posts(), 2)

        # User searchs on Python posts
        self.home_page.search_posts(terms, category_id=settings.PYTHON_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User searchs on Django posts
        self.home_page.search_posts(terms, category_id=settings.DJANGO_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

        # User searchs on Miscellaneous posts
        terms = '{} {}'.format(settings.PYTHON_CATEGORY, settings.MISCELLANEOUS_CATEGORY)
        self.home_page.search_posts(terms, category_id=settings.MISCELLANEOUS_CATEGORY)
        self.assertEqual(self.home_page.count_posts(), 1)

    def test_post_details(self):
        post = factories.PostFactory(
            author=self.user,
            status_id=settings.POST_PUBLIC_STATUS,
            content=settings.FUZZY_TEXTS[5])
        post.tags.add(
            factories.TagFactory(term='term0'),
            factories.TagFactory(term='term1'))
        factories.CommentFactory.create_batch(5, post=post)

        self.home_page.reload()
        post_element = self.home_page.get_post_details_by_pk(post.pk)

        self.assertEqual(post_element.get('author'), post.author.username)
        self.assertEqual(post_element.get('title'), post.title)
        self.assertEqual(post_element.get('num_comments'), str(5))
        self.assertEqual(post_element.get('created'), post.created.strftime('%B %d, %Y'))
        self.assertEqual(post_element.get('tags'), 'term0 term1')
        self.assertHTMLEqual(
            post_element.get('content'),
            '{}{}'.format(post.content[:settings.POST_TEXT_CONTENT_LIMIT-3], '...'))

    def test_post_content_must_be_truncated(self):
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)
        self.home_page.reload()
        post_element = self.home_page.get_post_details_by_pk(post.pk)
        self.assertLessEqual(len(post_element.get('content')), settings.POST_TEXT_CONTENT_LIMIT)

    def test_comments_link(self):
        post = factories.PostFactory(author=self.user, status_id=settings.POST_PUBLIC_STATUS)

        self.home_page.reload()
        self.home_page.click_on_num_comments_link(post.pk)

        self.assertEqual(
            '{}{}{}'.format(
                self.live_server_url,
                reverse('posts:detail', kwargs=dict(slug=post.slug)),
                '#comments_id'),
            self.home_page.current_driver_url)

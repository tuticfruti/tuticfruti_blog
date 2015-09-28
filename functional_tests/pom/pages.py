# -*- coding: utf-8 -*-
import re

from selenium.common.exceptions import TimeoutException

from django.core.urlresolvers import reverse

from .base_page import BasePage
from . import page_elements


class HomePage(BasePage):
    # Relative url
    url_path = reverse('home')

    # Web elements
    _home_page_link = page_elements.HomePageLink()
    _python_category_link = page_elements.PythonCategoryLink()
    _django_category_link = page_elements.DjangoCategoryLink()
    _miscellaneous_category_link = page_elements.MiscellaneousCategoryLink()
    _container = page_elements.Container()
    _prev_link = page_elements.PrevLink()
    _next_link = page_elements.NextLink()
    _search_form = page_elements.SearchForm()
    _search_form_input = page_elements.SearchFormInput()
    _search_form_button = page_elements.SearchFormButton()

    # Web element collections
    _posts = page_elements.PostCollection()

    @property
    def current_page(self):
        regex = re.search(r'\?page\=([0-9]+)', self.current_driver_url)
        try:
            return int(regex.group(1))
        except ValueError:
            return

    def goto_home_page(self):
        self._home_page_link.click()

    def select_category(self, category_id):
        category_link = getattr(self, '_{}_category_link'.format(category_id))
        category_link.click()

    def is_category_enabled(self, category_id):
        category_link = getattr(self, '_{}_category_link'.format(category_id))
        return 'active' in category_link.get_attribute('class')

    def count_posts(self):
        return len(self._posts)

    def search_posts(self, terms, category_id=None):
        if category_id:
            getattr(self, '_{}_category_link'.format(category_id)).click()
        self._search_form_input = terms
        self._search_form_button.click()

    def is_empty_message_visible(self):
        return 'Results were not found.' in self._container.text

    def is_prev_link_visible(self):
        try:
            return self._prev_link is not None
        except TimeoutException:
            return

    def is_next_link_visible(self):
        try:
            return self._next_link is not None
        except TimeoutException:
            return

    def goto_next_page(self):
        self._next_link.click()

    def goto_prev_page(self):
        self._prev_link.click()

    def goto_post(self, pk):
        self.click_on_read_me_link(pk)

    def click_on_read_me_link(self, pk):
        post_element = self._driver.find_element_by_id('post{}_id'.format(str(pk)))
        read_more_link = post_element.find_element_by_class_name('read_more')
        read_more_link.click()

    def click_on_num_comments_link(self, pk):
        post_element = self._driver.find_element_by_id('post{}_id'.format(str(pk)))
        comments_link = post_element.find_element_by_class_name('post_num_comments')
        comments_link.click()

    def _get_post_details(self, post_element):
        return dict(
            author=post_element.find_element_by_class_name('post_author').text,
            title=post_element.find_element_by_class_name('post_title').text,
            created=post_element.find_element_by_class_name('post_created').text,
            content=post_element.find_element_by_class_name('post_content').text,
            tags=post_element.find_element_by_class_name('post_tags').text,
            num_comments=post_element.find_element_by_class_name('post_num_comments').text)

    def get_post_details_by_pk(self, pk):
        post_element = self._driver.find_element_by_id('posts_id').find_element_by_id(
            'post{}_id'.format(str(pk)))
        return self._get_post_details(post_element)

    def get_post_details_by_key(self, key):
        post_element = self._posts[key]
        return self._get_post_details(post_element)


class PostDetailsPage(BasePage):
    # Web elements
    _post_details = page_elements.PostDetails()
    _comment_form = page_elements.CommentForm()
    _author_input = page_elements.AuthorInput()
    _email_input = page_elements.EmailInput()
    _content_textarea = page_elements.ContentTextarea()

    # Web element collections
    _comments = page_elements.CommentCollection()

    def __init__(self, liver_server_url, slug):
        self.url_path = reverse('posts:detail', kwargs=dict(slug=slug))
        super().__init__(liver_server_url)

    def send_comment_form(self, author, email, content):
        self._author_input = author
        self._email_input = email
        self._content_textarea = content
        self._comment_form.find_element_by_tag_name('button').click()

    def is_comment_displayed(self, content):
        for comment in self._comments:
            if (comment.text == content):
                return True

    def count_comments(self):
        return len(self._comments)

    def _get_comment_details(self, comment_element):
        return dict(
            created=comment_element.find_element_by_class_name('created').text,
            author=comment_element.find_element_by_class_name('author').text,
            content=comment_element.find_element_by_class_name('content').text)

    def get_comment_details_by_key(self, key):
        comment_element = self._comments[key]
        return self._get_comment_details(comment_element)

    def get_comment_details_by_pk(self, pk):
        comment_element = self._driver.find_element_by_id('comments_id').find_element_by_id(
            'comment{}_id'.format(str(pk)))
        return self._get_comment_details(comment_element)

    def get_post_details(self):
        post_element = self._driver.find_element_by_class_name('post')
        return dict(
            author=post_element.find_element_by_class_name('post_author').text,
            title=post_element.find_element_by_class_name('post_title').text,
            created=post_element.find_element_by_class_name('post_created').text,
            content=post_element.find_element_by_class_name('post_content').text,
            tags=post_element.find_element_by_class_name('post_tags').text,
            num_comments=post_element.find_element_by_class_name('post_num_comments').text)

    def is_empty_message_visible(self):
        return 'Results were not found.' in self._driver.find_element_by_id('comments_id').text

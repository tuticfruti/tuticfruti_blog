# -*- coding: utf-8 -*-
import re

from selenium.common.exceptions import TimeoutException

from .base_page import BasePage
from . import page_elements


class HomePage(BasePage):
    # Elements
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

    # Collections
    _posts = page_elements.PostCollection()

    @property
    def current_page(self):
        regex = re.search(r'\?page\=([0-9]+)', self.current_url)
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

    def get_post_details(self, key):
        post = self._posts[key]
        return dict(
            title=post.find_element_by_class_name('post_title').text,
            created=post.find_element_by_class_name('post_created').text,
            content=post.find_element_by_class_name('post_content').text,
            tags=post.find_element_by_class_name('post_tags').text, )

    def goto_post(self, title):
        for post in self._posts:
            if post.text == title:
                read_more_link = post.find_element_by_class_name('post_read_more')
                read_more_link.click()
                break

    def is_post_displayed(self, title):
        pass


class PostPage(BasePage):
    # Elements
    _comment_form = page_elements.CommentForm()
    _name_input = page_elements.NameInput()
    _email_input = page_elements.EmailInput()
    _comment_textarea = page_elements.ContentTextarea()

    # Collections
    _comments = page_elements.CommentCollection()

    def send_comment_form(self, comment):
        self._name_input = comment.name
        self._email_input = comment.email
        self._comment_textarea = comment.content
        self._comment_form.find_element_by_tag_name('button').click()

    def is_comment_displayed(self, content):
        for comment in self._comments:
            if (comment.text == content):
                return True

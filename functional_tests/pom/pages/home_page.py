# -*- coding: utf-8 -*-
import re

from .base_page import BasePage
from .. import page_elements


class HomePage(BasePage):
    # Elements
    _home_page_link = page_elements.HomePageLink()
    _python_category_link = page_elements.PythonCategoryLink()
    _django_category_link = page_elements.DjangoCategoryLink()
    _miscellaneous_category_link = page_elements.MiscellaneousCategoryLink()
    _container = page_elements.Container()
    _prev_link = page_elements.PrevLink()
    _next_link = page_elements.NextLink()

    # Collections
    _posts = page_elements.PostCollection()

    def __init__(self, driver, url):
        super().__init__(driver, url)

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

    def is_empty_message_visible(self):
        return 'Results were not found.' in self._container.text

    def is_prev_link_visible(self):
        return self._prev_link is not None

    def is_next_link_visible(self):
        return self._next_link is not None

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

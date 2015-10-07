# -*- coding: utf-8 -*-
import re

from selenium import webdriver

from functional_tests.pom import page_elements


class BasePage:
    _driver = None
    url = None
    url_path = None

    # Web elements

    # Web element collections
    _categories = page_elements.CategoryCollection()

    def __init__(self, live_server_url):
        self._driver = webdriver.Chrome()
        self.url = live_server_url + self.url_path

    @property
    def title(self):
        return self._driver.title

    @property
    def current_driver_url(self):
        return self._driver.current_url

    def open(self):
        self._driver.get(self.url)

    def close(self):
        self._driver.quit()

    def reload(self):
        self._driver.refresh()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _get_post_details(self, element):
        regex = re.search(r'post([0-9]+)_id', element.get_attribute('id'))
        return dict(
            id=int(regex.group(1)),
            pk=int(regex.group(1)),
            categories=element.find_element_by_class_name('post_categories').text,
            author=element.find_element_by_class_name('post_author').text,
            title=element.find_element_by_class_name('post_title').text,
            created=element.find_element_by_class_name('post_created').text,
            content=element.find_element_by_class_name('post_content').text,
            tags=element.find_element_by_class_name('post_tags').text,
            num_comments=element.find_element_by_class_name('comments__count').text)

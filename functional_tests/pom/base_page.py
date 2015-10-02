# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

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

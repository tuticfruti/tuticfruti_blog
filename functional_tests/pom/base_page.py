# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class BasePage:
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
        self._driver.get(self.url)

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def select_category(self, pk):
        category_element = self._driver.find_element_by_id('category{}_id'.format(str(pk)))
        category_element.click()

    def is_category_enabled(self, pk):
        category_element = self._driver.find_element_by_id('category{}_id'.format(str(pk)))
        return 'active' in category_element.get_attribute('class')

    def is_category_displayed(self, pk):
        try:
            category_element = self._driver.find_element_by_id('category{}_id'.format(str(pk)))
            if category_element:
                return True
        except NoSuchElementException:
            return

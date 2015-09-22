# -*- coding: utf-8 -*-
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 2  # seconds


class WebElement:
    def __get__(self, obj, type):
        wdw = WebDriverWait(obj._driver, TIMEOUT)
        wdw.until(
            lambda driver: driver.find_element(*self._locator),
            'Element {} not found'.format(self._locator))
        return obj._driver.find_element(*self._locator)

    def __set__(self, obj, value):
        wdw = WebDriverWait(obj._driver, TIMEOUT)
        wdw.until(
            lambda driver: driver.find_element(*self._locator),
            'Element {} not found'.format(self._locator))
        element = obj._driver.find_element(*self._locator)

        if element.tag_name in ['input', 'textarea']:
            element.clear()
            element.send_keys(value)


class WebElementCollection:
    def __get__(self, obj, type):
        wdw = WebDriverWait(obj._driver, TIMEOUT)
        wdw.until(
            lambda driver: driver.find_elements(*self._locator),
            'Element {} not found'.format(self._locator))
        self._elements = obj._driver.find_elements(*self._locator)
        return self._elements

# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 2  # seconds


class WebElement:
    def __get__(self, obj, type):
        try:
            wdw = WebDriverWait(obj._driver, TIMEOUT)
            wdw.until(lambda driver: driver.find_element(*self._locator))
            return obj._driver.find_element(*self._locator)
        except TimeoutException:
            return

    def __set__(self, obj, value):
        try:
            wdw = WebDriverWait(obj._driver, TIMEOUT)
            wdw.until(lambda driver: driver.find_element(*self._locator))
            element = obj._driver.find_element(*self._locator)
        except TimeoutException:
            return

        if element.tag_name == 'input':
            element.clear()
            element.send_keys(value)


class WebElementCollection:
    def __get__(self, obj, type):
        try:
            wdw = WebDriverWait(obj._driver, TIMEOUT)
            wdw.until(lambda driver: driver.find_elements(*self._locator))
            self._elements = obj._driver.find_elements(*self._locator)
            return self._elements
        except TimeoutException:
            return

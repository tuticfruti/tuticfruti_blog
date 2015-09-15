# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

TIMEOUT = 2  # In seconds


class WebElement:
    def __get__(self, instance, instance_class):
        try:
            wdw = WebDriverWait(instance._driver, TIMEOUT)
            wdw.until(lambda driver: driver.find_element(*self._locator))
            return instance._driver.find_element(*self._locator)
        except TimeoutException:
            return


class WebElementCollection:
    def __get__(self, instance, instance_class):
        try:
            wdw = WebDriverWait(instance._driver, TIMEOUT)
            wdw.until(lambda driver: driver.find_elements(*self._locator))
            return instance._driver.find_elements(*self._locator)
        except TimeoutException:
            return

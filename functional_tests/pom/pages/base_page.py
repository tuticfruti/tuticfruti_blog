# -*- coding: utf-8 -*-
class BasePage:
    def __init__(self, driver, url):
        self._driver = driver
        self._url = url
        self._driver.get(self._url)

    @property
    def title(self):
        return self._driver.title

    @property
    def current_url(self):
        return self._driver.current_url

    def reload(self):
        self._driver.get(self._url)

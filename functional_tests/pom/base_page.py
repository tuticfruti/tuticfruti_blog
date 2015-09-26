# -*- coding: utf-8 -*-
from selenium import webdriver


class BasePage:
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

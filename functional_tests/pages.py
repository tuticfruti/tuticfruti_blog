# -*- coding: utf-8 -*-
from .selenium_driver import SeleniumDriver
from .page_elements import *


class BasePage:

    def __init__(self, url):
        self.url = url

    def load(self):
        SeleniumDriver.driver.get(self.url)

    def get_title(self):
        return SeleniumDriver.driver.title


class HomePage(BasePage):
    # Web elements
    home_link = HomeLink()
    python_category_link = PythonCategoryLink()
    django_category_link = DjangoCategoryLink()
    miscellaneous_category_link = MiscellaneousCategoryLink()

    # Web elements collections
    posts = PostsCollection()

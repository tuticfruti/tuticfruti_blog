# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


class CommonLocators:
    HOME_LINK = (By.XPATH, '//nav[@id="navbar-top"]//a[contains(@class,"navbar-brand")]')
    PYTHON_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[1]/a')
    DJANGO_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[2]/a')
    MISCELLANEOUS_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[3]/a')

    POSTS = (By.XPATH, '//div[contains(@class, "post")]')

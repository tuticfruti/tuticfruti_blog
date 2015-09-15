# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


HOME_PAGE_LINK = (By.XPATH, '//nav[@id="navbar-top"]//a[contains(@class,"navbar-brand")]')
PYTHON_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[1]/a')
DJANGO_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[2]/a')
MISCELLANEOUS_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[3]/a')
PREV_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-prev")]/a')
NEXT_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-next")]/a')
CONTAINER = (By.XPATH, '//div[contains(@class, "container")]')

POSTS = (By.XPATH, '//div[contains(@class, "post")]')

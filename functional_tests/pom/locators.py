# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By


HOME_PAGE_LINK = (By.XPATH, '//nav[@id="navbar-top"]//a[contains(@class,"navbar-brand")]')
PYTHON_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[1]/a')
DJANGO_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[2]/a')
MISCELLANEOUS_CATEGORY_LINK = (By.XPATH, '//nav[@id="navbar-top"]//ul[contains(@class,"navbar-nav")]/li[3]/a')
PREV_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-prev")]/a')
NEXT_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-next")]/a')
CONTAINER = (By.XPATH, '//div[contains(@class, "container")]')
SEARCH_FORM = (By.XPATH, '//form[@id="search_form"]')
SEARCH_FORM_INPUT = (By.XPATH, '//form[@id="search_form"]//input')
SEARCH_FORM_BUTTON = (By.XPATH, '//form[@id="search_form"]//button')
COMMENT_FORM = (By.XPATH, '//form[@id="comment_form"]')
NAME_INPUT = (By.NAME, 'name')
EMAIL_INPUT = (By.NAME, 'email')
CONTENT_TEXTAREA = (By.NAME, 'content')

POSTS = (By.XPATH, '//div[contains(@class, "post")]')
COMMENTS = (By.XPATH, '//div[contains(@class, "comment")]')

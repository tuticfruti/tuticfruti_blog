# -*- coding: utf-8 -*-
from selenium.webdriver.common.by import By

# Element locators
HOME_PAGE_LINK = (By.XPATH, '//nav[@id="navbar-top"]//a[contains(@class,"navbar-brand")]')
PREV_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-prev")]/a')
NEXT_LINK = (By.XPATH, '//nav[@id="pagination"]//li[contains(@class, "pager-next")]/a')
CONTAINER = (By.XPATH, '//div[contains(@class, "container")]')
SEARCH_FORM = (By.XPATH, '//form[@id="search_form_id"]')
SEARCH_FORM_INPUT = (By.XPATH, '//form[@id="search_form_id"]//input')
SEARCH_FORM_BUTTON = (By.XPATH, '//form[@id="search_form_id"]//button')
COMMENT_FORM = (By.XPATH, '//form[@id="comment_form_id"]')
AUTHOR_INPUT = (By.XPATH, '//input[@name="author"]')
EMAIL_INPUT = (By.XPATH, '//input[@name="email"]')
CONTENT_TEXTAREA = (By.XPATH, '//textarea[@name="content"]')
POST_DETAILS = (By.XPATH, '//div[contains(@class, "post")]')

# Element colletion locators
POSTS = (By.XPATH, '//div[contains(@class, "post")]')
COMMENTS = (By.XPATH, '//div[contains(@class, "comment")]')
CATEGORIES = (By.XPATH, '//ul[@id="categories_id"]//a[contains(@class, "category")]')

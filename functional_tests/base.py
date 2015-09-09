# -*- coding: utf-8 -*-
from selenium import webdriver

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .selenium_driver import SeleniumDriver


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        SeleniumDriver.open()
        print(SeleniumDriver.driver)

    @classmethod
    def tearDownClass(cls):
        SeleniumDriver.close()
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        pass

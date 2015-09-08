# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .selenium_driver import SeleniumDriver


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        SeleniumDriver().driver.quit()
        super(FunctionalTest, cls).setUpClass()

    @classmethod
    def setUpTestData(cls):
        pass

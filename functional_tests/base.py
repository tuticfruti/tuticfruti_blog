# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from .selenium_driver import SeleniumDriver


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        SeleniumDriver.open()

    @classmethod
    def tearDownClass(cls):
        SeleniumDriver.close()
        super().setUpClass()

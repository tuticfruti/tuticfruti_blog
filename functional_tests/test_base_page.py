# -*- coding: utf-8 -*-
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from tuticfruti_blog.users import UserFactory
from tuticfruti_blog.posts import factories


class BasePageTest(StaticLiveServerTestCase):
    page = None

    def setUp(self, page):
        self.user = UserFactory()
        self.python_category = factories.CategoryFactory('Python')
        self.python_django = factories.CategoryFactory('Django')
        self.python_miscellaneous = factories.CategoryFactory('Miscellaneous')
        self.page = page
        self.page.open()

    def tearDown(self):
        self.page.close()

    def test_all_active_categories_are_present(self):
        pass

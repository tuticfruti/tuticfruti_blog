from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from tuticfruti_blog.users.factories import UserFactory
from tuticfruti_blog.posts import factories


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.python_category = factories.CategoryFactory(name='Python')
        cls.django_category = factories.CategoryFactory(name='Django')
        cls.miscellaneous_category = factories.CategoryFactory(name='Miscellaneous')

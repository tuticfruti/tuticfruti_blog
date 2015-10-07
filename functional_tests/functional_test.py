from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from tuticfruti_blog.core import data_fixtures
from tuticfruti_blog.posts import models


class FunctionalTest(StaticLiveServerTestCase):
    @classmethod
    def setUpTestData(cls):
        # Load base data
        data_fixtures.DataFixtures.load()

        # Users
        cls.user = models.User.objects.get(username='user0')

        # Posts
        cls.published_posts = models.Post.objects.all_published()
        cls.draft_post = models.Post.objects.get(slug='draft-post')
        cls.published_post = models.Post.objects.get(slug='published-post')
        cls.post_without_comments = models.Post.objects \
            .filter(comments__isnull=True) \
            .first()
        cls.python_post = models.Post.objects.get(slug='python-post')
        cls.django_post = models.Post.objects.get(slug='django-post')
        cls.miscellaneous = models.Post.objects.get(slug='miscellaneous-post')

        # Categories
        cls.enabled_categories = models.Category.objects.all_enabled()
        cls.first_category = models.Category.objects.get(slug='first-category')
        cls.python_category = models.Category.objects.get(slug='python')
        cls.django_category = models.Category.objects.get(slug='django')
        cls.miscellaneous_category = models.Category.objects.get(
            slug='miscellaneous')
        cls.disabled_category = models.Category.objects.get(is_enabled=False)

        # Tags
        cls.tags = models.Tag.objects.all()
        cls.python_tag = models.Tag.objects.get(term='python')
        cls.django_tag = models.Tag.objects.get(term='django')
        cls.miscellaneous_tag = models.Tag.objects.get(term='miscellaneous')

        # Comments
        cls.published_comments = cls.published_post.comments.all_published()
        cls.published_comment = models.Comment.objects.get(author='anonymous')
        cls.pending_comment = models.Comment.objects.get(content='Pending comment')

import datetime

from django.utils import timezone

from tuticfruti_blog.users.models import User
from tuticfruti_blog.posts import factories
from tuticfruti_blog.posts import models


class RegistryHolder(type):
    REGISTRY = {}

    def __new__(cls, name, bases, attrs):
        new_cls = super(RegistryHolder, cls).__new__(cls, name, bases, attrs)
        if new_cls.__name__ != 'DataFixtures':
            cls.REGISTRY[new_cls.get_order()] = new_cls
        return new_cls

    @classmethod
    def get_registry(cls):
        return dict(cls.REGISTRY)


class DataFixtures(metaclass=RegistryHolder):
    @staticmethod
    def load():
        for key in sorted(RegistryHolder.get_registry()):
            RegistryHolder.get_registry().get(key).load()


class LoadUserData(DataFixtures):
    @staticmethod
    def load():
        User.objects.create_user(username='user0')

    @staticmethod
    def get_order():
        return 1


class LoadCategoryData(DataFixtures):
    @staticmethod
    def load():
        factories.CategoryFactory(name='First category', order=-1)
        factories.CategoryFactory(name='Miscellaneous', order=3)
        factories.CategoryFactory(name='Django', order=2)
        factories.CategoryFactory(name='Python', order=1)
        factories.CategoryFactory(
            name='Disabled category', is_enabled=False, order=4)

    @staticmethod
    def get_order():
        return 2


class LoadTagData(DataFixtures):
    @staticmethod
    def load():
        factories.TagFactory(term='python')
        factories.TagFactory(term='django')
        factories.TagFactory(term='miscellaneous')

    @staticmethod
    def get_order():
        return 3


class LoadPostData(DataFixtures):
    @staticmethod
    def load():
        user = User.objects.get(username='user0')
        categories = models.Category.objects.all()
        tags = models.Tag.objects.all()

        # Creates PAGINATE_BY
        factories.PostFactory.create_batch(
            models.Post.PAGINATE_BY,
            author=User.objects.get(username='user0'),
            status_id=models.Post.STATUS_PUBLISHED)

        # Published post
        factories.PostFactory(
            author=User.objects.get(username='user0'),
            title='Published post',
            status_id=models.Post.STATUS_PUBLISHED,
            categories=categories,
            tags=tags,
            content=factories.FUZZY_TEXTS[5]  # Size > TEXT_CONTENT_LIMIT
            )

        # Draft post
        factories.PostFactory(
            title='Draft post',
            author=user,
            status_id=models.Post.STATUS_DRAFT)

        # Python post
        factories.PostFactory(
            title='Python post',
            author=user,
            status_id=models.Post.STATUS_PUBLISHED,
            categories=[categories.get(slug='python')],
            tags=[tags.get(term='python')])

        # Django post
        factories.PostFactory(
            title='Django post',
            author=user,
            status_id=models.Post.STATUS_PUBLISHED,
            categories=[categories.get(slug='django')],
            tags=[tags.get(term='django')])

        # Miscellaneous post
        factories.PostFactory(
            title='Miscellaneous post',
            author=user,
            status_id=models.Post.STATUS_PUBLISHED,
            categories=[categories.get(slug='miscellaneous')],
            tags=[tags.get(term='miscellaneous')])

    @staticmethod
    def get_order():
        return 4


class LoadCommentData(DataFixtures):
    @staticmethod
    def load():
        post = models.Post.objects.get(slug='published-post')
        factories.CommentFactory.create_batch(
            9,
            post=post,
            status_id=models.Comment.STATUS_PUBLISHED)
        factories.CommentFactory(
            post=post,
            status_id=models.Comment.STATUS_PUBLISHED,
            author='anonymous',
            email='anonymonus@example.com',
            content='Published comment')
        factories.CommentFactory(
            post=post,
            status_id=models.Comment.STATUS_PENDING,
            content='Pending comment')

    @staticmethod
    def get_order():
        return 5

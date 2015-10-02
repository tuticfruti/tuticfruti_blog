# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from tuticfruti_blog.users.models import User


class Tag(models.Model):
    term = models.CharField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if self.term:
            self.term = self.term.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.term


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False)
    slug = models.SlugField(max_length=25)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    TEXT_CONTENT_LIMIT = 255

    PAGINATE_BY = 10
    PAGINATE_ORPHANS = 1
    ORDERING = '-created'

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = (
        (STATUS_DRAFT, 'Draft'),
        (STATUS_PUBLISHED, 'Published'),
    )

    categories = models.ManyToManyField(Category, related_name='posts')
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    content = models.TextField(blank=True)
    status_id = models.CharField(
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        max_length=10,
        db_index=True)
    tags = models.ManyToManyField(Tag, related_name='posts')
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    ORDERING = '-created'
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pending'),
        (STATUS_PUBLISHED, 'Published'),
    )

    post = models.ForeignKey(Post, related_name='comments')
    status_id = models.CharField(
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        max_length=10,
        db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(db_index=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    def __str__(self):
        return self.content

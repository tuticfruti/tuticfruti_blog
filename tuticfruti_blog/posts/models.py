# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from tuticfruti_blog.users.models import User
from tuticfruti_blog.core import settings


class Tag(models.Model):
    term = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.term


class Post(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255, unique=True)
    slug = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    status_id = models.CharField(
        choices=settings.POST_STATUS_CHOICES,
        default=settings.POST_DRAFT_STATUS,
        max_length=10,
        db_index=True)
    category_id = models.CharField(
        choices=settings.CATEGORY_CHOICES,
        default=settings.PYTHON_CATEGORY,
        max_length=20,
        db_index=True)
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post)
    status_id = models.CharField(
        choices=settings.COMMENT_STATUS_CHOICES,
        default=settings.COMMENT_PENDING_STATUS,
        max_length=10,
        db_index=True)
    author = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(db_index=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    def __str__(self):
        return self.content

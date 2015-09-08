# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.conf import settings


class Post(models.Model):

    DRAFT_STATUS = 'draft'
    PUBLIC_STATUS = 'public'
    STATUS = (
        (DRAFT_STATUS, 'Draft'),
        (PUBLIC_STATUS, 'Public'),
    )

    PYTHON_CATEGORY = 'python'
    DJANGO_CATEGORY = 'django'
    MISCELLANEOUS_CATEGORY = 'miscellaneous'
    CATEGORIES = (
        (PYTHON_CATEGORY, 'Python'),
        (DJANGO_CATEGORY, 'Django'),
        (MISCELLANEOUS_CATEGORY, 'Miscellaneous'),
    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    status_id = models.CharField(choices=STATUS, default=DRAFT_STATUS, max_length=10, db_index=True)
    category_id = models.CharField(choices=CATEGORIES, default=PYTHON_CATEGORY, max_length=20)
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug, })

    def __str__(self):
        return self.title

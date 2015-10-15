# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from tuticfruti_blog.posts import managers
from tuticfruti_blog.users.models import User


class Tag(models.Model):
    term = models.CharField(max_length=255, unique=True, verbose_name=_('term'))

    def __str__(self):
        return self.term

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['term']


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, verbose_name=_('name'))
    slug = models.SlugField(max_length=100, verbose_name=_('slug'))
    order = models.IntegerField(default=0, verbose_name=_('order'))
    is_enabled = models.BooleanField(default=True, verbose_name=_('is enabled'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    objects = managers.CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order']


class Post(models.Model):
    HR = '<hr />'
    PAGINATE_BY = 10
    PAGINATE_ORPHANS = 1

    STATUS_DRAFT = 'draft'
    STATUS_PUBLISHED = 'published'

    STATUS_CHOICES = (
        (STATUS_DRAFT, _('draft')),
        (STATUS_PUBLISHED, _('published')),
    )

    categories = models.ManyToManyField(Category, related_name='posts', verbose_name=_('categories'))
    author = models.ForeignKey(User, related_name='posts', verbose_name=_('author'))
    title = models.CharField(max_length=255, unique=True, verbose_name=_('title'))
    slug = models.SlugField(max_length=255, db_index=True, verbose_name=_('slug'))
    content = RichTextUploadingField(blank=True, verbose_name=_('content'))
    status_id = models.CharField(
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
        max_length=10,
        db_index=True, verbose_name=_('status'))
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name=_('tags'))
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True, verbose_name=_('modified'))

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    objects = managers.PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created']


class Comment(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_CHOICES = (
        (STATUS_PENDING, _('pending')),
        (STATUS_PUBLISHED, _('published')), )

    post = models.ForeignKey(Post, related_name='comments', verbose_name=_('post'))
    status_id = models.CharField(
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        max_length=10,
        db_index=True, verbose_name=_('status'))
    author = models.CharField(max_length=100, db_index=True, verbose_name=_('author'))
    email = models.EmailField(db_index=True, verbose_name=_('email'))
    content = models.TextField(verbose_name=_('content'))
    created = models.DateTimeField(auto_now_add=True, blank=True, db_index=True, verbose_name=_('created'))
    modified = models.DateTimeField(auto_now=True, blank=True, db_index=True, verbose_name=_('created'))

    def __str__(self):
        return self.content

    objects = managers.CommentManager()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ["-created"]

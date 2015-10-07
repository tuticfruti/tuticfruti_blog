# -*- coding: utf-8 -*-
from django.db import models


class PostManager(models.Manager):
    def all_published(self):
        return self.filter(status_id=self.model.STATUS_PUBLISHED)

    def all_draft(self):
        return self.filter(status_id=self.model.STATUS_DRAFT)


class CommentManager(models.Manager):
    def all_published(self):
        return self.filter(status_id=self.model.STATUS_PUBLISHED)

    def all_pending(self):
        return self.filter(status_id=self.model.STATUS_PENDING)


class CategoryManager(models.Manager):
    def all_enabled(self):
        return self.filter(is_enabled=True)

    def all_disabled(self):
        return self.filter(is_enabled=False)

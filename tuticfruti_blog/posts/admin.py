# -*- coding: utf-8 -*-
from django.contrib import admin

from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField

from . import models


admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Category)

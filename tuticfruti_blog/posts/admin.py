# -*- coding: utf-8 -*-
from django.contrib import admin

from . import models


admin.site.register(models.Post)
admin.site.register(models.Tag)
admin.site.register(models.Comment)

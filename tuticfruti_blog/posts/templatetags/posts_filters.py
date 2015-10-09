# -*- coding: utf-8 -*-
import re

from django import template
from django.template.defaultfilters import stringfilter
from .. import models

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def hr_truncate(value, arg):
    search_result = re.search(models.Post.HR, value)
    if search_result and arg == 'left':
        value = value[:search_result.start()]
    if search_result and arg == 'right':
        value = value[search_result.start() + len(models.Post.HR):]

    return value

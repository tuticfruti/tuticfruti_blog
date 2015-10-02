# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20150930_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='tags',
        ),
    ]

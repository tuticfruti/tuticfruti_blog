# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_category_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category_id',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=1, related_name='posts', to='posts.Category'),
            preserve_default=False,
        ),
    ]

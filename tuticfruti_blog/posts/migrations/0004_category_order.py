# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150930_0940'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]

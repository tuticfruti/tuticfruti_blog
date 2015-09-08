# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20150905_0845'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='category',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='status',
            new_name='status_id',
        ),
    ]

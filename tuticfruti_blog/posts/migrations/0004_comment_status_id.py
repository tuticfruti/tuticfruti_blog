# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150922_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='status_id',
            field=models.CharField(db_index=True, max_length=10, choices=[('pending', 'Pending'), ('published', 'Published')], default='pending'),
        ),
    ]

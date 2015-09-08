# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150903_1758'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.CharField(max_length=20, default='python', choices=[('python', 'Python'), ('django', 'Django'), ('miscellaneous', 'Miscellaneous')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(max_length=10, default='draft', db_index=True, choices=[('draft', 'Draft'), ('public', 'Public')]),
        ),
    ]

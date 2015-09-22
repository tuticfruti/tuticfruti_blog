# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
            ],
        ),
        migrations.AlterField(
            model_name='post',
            name='status_id',
            field=models.CharField(default='draft', db_index=True, choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10),
        ),
    ]

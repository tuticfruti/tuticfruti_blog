# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=255, db_index=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('content', models.TextField(blank=True)),
                ('status_id', models.CharField(max_length=10, default='draft', db_index=True, choices=[('draft', 'Draft'), ('public', 'Public')])),
                ('category_id', models.CharField(max_length=20, choices=[('python', 'Python'), ('django', 'Django'), ('miscellaneous', 'Miscellaneous')], default='python')),
                ('tags', models.CharField(max_length=255, db_index=True)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]

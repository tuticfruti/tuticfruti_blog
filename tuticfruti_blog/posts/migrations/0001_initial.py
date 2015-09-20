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
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255, db_index=True)),
                ('slug', models.CharField(unique=True, max_length=255)),
                ('content', models.TextField(blank=True)),
                ('status_id', models.CharField(choices=[('draft', 'Draft'), ('public', 'Public')], default='draft', max_length=10, db_index=True)),
                ('category_id', models.CharField(choices=[('python', 'Python'), ('django', 'Django'), ('miscellaneous', 'Miscellaneous')], default='python', max_length=20)),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('term', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='posts.Tag'),
        ),
    ]

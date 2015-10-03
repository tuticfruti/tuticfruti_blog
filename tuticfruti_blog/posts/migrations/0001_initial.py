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
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=25)),
                ('order', models.IntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('status_id', models.CharField(db_index=True, choices=[('pending', 'Pending'), ('published', 'Published')], max_length=10, default='pending')),
                ('author', models.CharField(db_index=True, max_length=100)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255)),
                ('content', models.TextField(blank=True)),
                ('status_id', models.CharField(db_index=True, choices=[('draft', 'Draft'), ('published', 'Published')], max_length=10, default='draft')),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='posts')),
                ('categories', models.ManyToManyField(to='posts.Category', related_name='posts')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('term', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['term'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='posts.Tag', related_name='posts'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(to='posts.Post', related_name='comments'),
        ),
    ]

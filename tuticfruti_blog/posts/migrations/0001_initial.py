# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(max_length=25)),
                ('order', models.IntegerField(default=0)),
                ('is_enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'categories',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('status_id', models.CharField(max_length=10, db_index=True, default='pending', choices=[('pending', 'Pending'), ('published', 'Published')])),
                ('author', models.CharField(max_length=100, db_index=True)),
                ('email', models.EmailField(max_length=254, db_index=True)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField(max_length=255)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                ('status_id', models.CharField(max_length=10, db_index=True, default='draft', choices=[('draft', 'Draft'), ('published', 'Published')])),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(db_index=True, auto_now=True)),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
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

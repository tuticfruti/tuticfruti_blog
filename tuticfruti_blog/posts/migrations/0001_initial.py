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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=100)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('status_id', models.CharField(choices=[('pending', 'Pending'), ('published', 'Published')], db_index=True, default='pending', max_length=10)),
                ('author', models.CharField(db_index=True, max_length=100)),
                ('email', models.EmailField(db_index=True, max_length=254)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(unique=True, max_length=255)),
                ('slug', models.CharField(unique=True, max_length=255)),
                ('content', models.TextField(blank=True)),
                ('status_id', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], db_index=True, default='draft', max_length=10)),
                ('category_id', models.CharField(choices=[('python', 'Python'), ('django', 'Django'), ('miscellaneous', 'Miscellaneous')], db_index=True, default='python', max_length=20)),
                ('created', models.DateTimeField(db_index=True, auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True, db_index=True)),
                ('author', models.ForeignKey(related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('term', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='posts.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(related_name='comments', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='category',
            name='tags',
            field=models.ManyToManyField(related_name='categories', to='posts.Tag'),
        ),
    ]

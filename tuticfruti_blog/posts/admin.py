# -*- coding: utf-8 -*-
from django.db.models import Prefetch
from django.contrib import admin
from django.template.defaultfilters import striptags, truncatewords

from . import models


class CommentInline(admin.TabularInline):
    model = models.Comment


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    def _categories(self, obj):
        return obj.categories.values_list('name', flat=True)

    def _tags(self, obj):
        return obj.tags.values_list('term', flat=True)

    def num_comments(self, obj):
        return obj.comments.count()

    date_hierarchy = 'created'
    fields = (('title', 'created', ), ('author', 'status_id', ), 'content', 'tags', 'categories', )
    filter_horizontal = ('categories', 'tags', )
    list_display = ('title', 'author', 'status_id', 'created', '_categories', '_tags', 'num_comments', )
    list_editable = ('status_id', )
    list_filter = ('status_id', 'categories', 'tags', 'author', 'created')
    search_fields = ('title', )
    readonly_fields = ('created', )
    inlines = [CommentInline, ]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['author'].initial = request.user
        return form

    def get_queryset(self, request):
        categories = models.Category.objects.all_enabled()
        tags = models.Tag.objects.all()
        comments = models.Comment.objects.all()

        qs = models.Post.objects \
            .all() \
            .prefetch_related(
                Prefetch('categories', queryset=categories),
                Prefetch('comments', queryset=comments),
                Prefetch('tags', queryset=tags))

        return qs


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('term', )
    list_display = ('term', )
    search_fields = ('term', )
    list_editable = ('term', )
    list_display_links = None


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'is_enabled', 'order', )
    list_display = ('name', 'is_enabled', 'order', )
    list_editable = ('is_enabled', 'order', )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    fields = (('author', 'created', ), ('email', 'status_id', ), 'content', )
    list_display = ('author', 'email', 'status_id', 'created', 'content', )
    list_editable = ('status_id', )
    list_filter = ('status_id', 'created')
    search_fields = ('author', 'email', 'content', )
    readonly_fields = ('created', )

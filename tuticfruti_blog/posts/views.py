# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from tuticfruti_blog.core import settings
from . import models


class PostListView(ListView):
    model = models.Post
    context_object_name = 'post_list'
    template_name = 'posts/home.html'
    ordering = settings.ORDERING
    paginate_by = settings.PAGINATE_BY
    paginate_orphans = settings.PAGINATE_ORPHANS

    def get_queryset(self):
        return models.Post.objects.filter(status_id=settings.POST_PUBLIC_STATUS)


class PostListByCategoryView(PostListView):
    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = models.Post.objects.filter(
                status_id=settings.POST_PUBLIC_STATUS,
                category_id=category_id)
        else:
            queryset = super().get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


class PostListSearchView(PostListView):
    def get_queryset(self):
        terms = self.request.GET.get('search_terms').split()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = models.Post.objects.filter(
                category_id=category_id,
                status_id=settings.POST_PUBLIC_STATUS,
                tags__term__in=terms).distinct()
        else:
            queryset = models.Post.objects.filter(
                status_id=settings.POST_PUBLIC_STATUS,
                tags__term__in=terms).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category_id'] = self.kwargs.get('category_id')
        context['search_terms'] = self.request.GET.get('search_terms')
        return context


class PostDetailView(DetailView):
    model = models.Post

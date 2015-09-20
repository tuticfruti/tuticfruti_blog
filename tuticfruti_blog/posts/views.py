# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from tuticfruti_blog.core.settings import PAGINATE_BY, PAGINATE_ORPHANS, ORDERING
from . import models


class PostListView(ListView):
    model = models.Post
    context_object_name = 'post_list'
    template_name = 'posts/home.html'
    ordering = ORDERING
    paginate_by = PAGINATE_BY
    paginate_orphans = PAGINATE_ORPHANS

    def _get_queryset_by_tags(self, category_id=None):
        terms = self.request.GET.get('search_terms').split()
        if category_id:
            queryset = models.Post.objects.filter(category_id=category_id, tags__term__in=terms).distinct()
        else:
            queryset = models.Post.objects.filter(tags__term__in=terms).distinct()
        return queryset

    def get_queryset(self):
        category_id = self.kwargs.get('category_id', None)
        search_terms = self.request.GET.get('search_terms', None)
        if search_terms:
            queryset = self._get_queryset_by_tags(category_id)
        elif category_id:
            queryset = models.Post.objects.filter(category_id=category_id)
        else:
            queryset = models.Post.objects.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category_id'] = self.kwargs.get('category_id', None)
        context['search_terms'] = self.request.GET.get('search_terms')
        return context


class PostDetailView(DetailView):
    model = models.Post

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

    def get_queryset(self):
        queryset = models.Post.objects.all()
        if self.kwargs.get('category_id'):
            queryset = models.Post.objects.filter(category_id=self.kwargs.get('category_id'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


class PostDetailView(DetailView):
    model = models.Post

# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView

from .models import Post


class BaseListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'posts/home.html'
    paginate_by = 10
    ordering = '-created'


class HomePageView(BaseListView):
    queryset = Post.objects.all()


class PostListView(BaseListView):
    def get_queryset(self):
        return Post.objects.all().filter(category_id=self.kwargs.get('category_id'))


class PostDetailView(DetailView):
    model = Post

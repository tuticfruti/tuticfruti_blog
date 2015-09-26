# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from django.db.models import Count

from tuticfruti_blog.core import settings
from . import models


class PostListView(ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = settings.PAGINATE_BY
    paginate_orphans = settings.PAGINATE_ORPHANS

    def get_queryset(self):
        return models.Post.objects \
            .annotate(num_comments=Count('comment')) \
            .filter(status_id=settings.POST_PUBLIC_STATUS) \
            .order_by(settings.ORDERING)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_text_content_limit'] = settings.POST_TEXT_CONTENT_LIMIT
        return context


class PostListByCategoryView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category_id'] = self.kwargs.get('category_id')
        return context


class PostListSearchView(PostListByCategoryView):
    def get_queryset(self):
        queryset = super().get_queryset()
        terms = self.request.GET.get('search_terms').split()
        queryset = queryset.filter(tags__term__in=terms).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_terms'] = self.request.GET.get('search_terms')
        return context


class PostDetailView(DetailView):
    model = models.Post
    context_object_name = 'post'
    template_name = 'posts/details.html'

    def post(self, request, slug):
        from django.http import HttpResponse
        from django.core.urlresolvers import reverse
        models.Comment.objects.create(
            post=self.get_object(),
            author=self.request.POST.get('author'),
            email=self.request.POST.get('email'),
            content=self.request.POST.get('content'))
        return HttpResponse(reverse('posts:details', kwargs=dict(slug=slug)))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.request.POST.get('author')
        context['email'] = self.request.POST.get('email')
        context['content'] = self.request.POST.get('content')
        context['comments'] = self.get_object().comment_set.all().order_by(settings.ORDERING)

        return context

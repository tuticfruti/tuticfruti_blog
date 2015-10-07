# -*- coding: utf-8 -*-
from django.views import generic as generic_views
from django.views.generic import edit as edit_mixins
from django.db.models import Prefetch
from django.core.urlresolvers import reverse

from . import models
from . import forms


class PostListView(generic_views.ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = models.Post.PAGINATE_BY
    paginate_orphans = models.Post.PAGINATE_ORPHANS

    def get_queryset(self):
        queryset = models.Post.objects \
            .all_published() \
            .prefetch_related(
                Prefetch('categories', queryset=models.Category.objects.all()),
                Prefetch('tags', queryset=models.Tag.objects.all()),
                Prefetch('comments', queryset=models.Comment.objects.all_published())) \
            .select_related('author')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_text_content_limit'] = models.Post.TEXT_CONTENT_LIMIT
        context['categories'] = models.Category.objects.all_enabled()
        return context


class PostListByCategoryView(PostListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            queryset = queryset.filter(categories__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_category'] = self.kwargs.get('slug')
        return context


class PostListSearchView(PostListByCategoryView):
    def get_queryset(self):
        queryset = super().get_queryset()
        terms = self.request.GET.get('search_terms').lower().split()
        queryset = queryset.filter(tags__term__in=terms).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_terms'] = self.request.GET.get('search_terms')
        return context


class PostDetailView(edit_mixins.FormMixin, generic_views.DetailView):
    template_name = 'posts/detail.html'
    form_class = forms.CommentForm
    context_object_name = 'post'

    def get_queryset(self):
        queryset = models.Post.objects \
            .filter(slug=self.kwargs.get('slug')) \
            .prefetch_related(
                Prefetch('comments', queryset=models.Comment.objects.all_published()),
                Prefetch('tags', queryset=models.Tag.objects.all()),
                Prefetch('categories', queryset=models.Category.objects.all_enabled())) \
            .select_related('author')
        return queryset

    def get_success_url(self):
        return reverse('posts:detail', kwargs=dict(slug=self.get_object().slug))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['categories'] = models.Category.objects.all_enabled()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        models.Comment.objects.create(
            post=self.get_object(),
            author=form['author'].value(),
            email=form['email'].value(),
            content=form['content'].value())
        return super().form_valid(form)

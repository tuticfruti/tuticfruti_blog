# -*- coding: utf-8 -*-
from django.views import generic as generic_views
from django.views.generic import detail as detail_mixins
from django.views.generic import edit as edit_mixins

from django.db.models import Count
from django.core.urlresolvers import reverse

from tuticfruti_blog.core import settings
from . import models
from . import forms


class PostListView(generic_views.ListView):
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


class PostDetailView(edit_mixins.FormMixin, generic_views.DetailView):
    model = models.Post
    template_name = 'posts/detail.html'
    form_class = forms.CommentForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('posts:detail', kwargs=dict(slug=self.get_object().slug))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['comments'] = self.get_object().comment_set.all().order_by(settings.ORDERING)
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

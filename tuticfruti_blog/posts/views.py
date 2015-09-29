# -*- coding: utf-8 -*-
from django.views import generic as generic_views
from django.views.generic import edit as edit_mixins
from django.db.models import Sum, Case, When, IntegerField
from django.core.urlresolvers import reverse

from tuticfruti_blog.core import settings
from . import models
from . import forms


class PostListView(generic_views.ListView):
    model = models.Post
    context_object_name = 'posts'
    template_name = 'posts/list.html'
    paginate_by = models.Post.PAGINATE_BY
    paginate_orphans = models.Post.PAGINATE_ORPHANS

    def get_queryset(self):
        return_value = models.Post.objects \
            .annotate(comments__count=Sum(
                Case(
                    When(comments__status_id=models.Comment.STATUS_PUBLISHED, then=1),
                    default=0,
                    output_field=IntegerField()))) \
            .filter(status_id=models.Post.STATUS_PUBLISHED) \
            .order_by(models.Post.ORDERING)

        return return_value

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_text_content_limit'] = models.Post.TEXT_CONTENT_LIMIT
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
        context['comments'] = self.get_object() \
            .comments.filter(status_id=models.Comment.STATUS_PUBLISHED) \
            .order_by(models.Post.ORDERING)
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

# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /posts/
    url(r'^$', views.PostListView.as_view(), name='list'),
    # ex: /posts/search/
    url(r'^search/$', views.PostListSearchView.as_view(), name='search'),
    # ex: /posts/python/search/
    url(r'^(?P<category_id>[a-z]+)/search/$', views.PostListSearchView.as_view(), name='search_category'),
    # ex: /posts/python/
    url(r'^(?P<category_id>[a-z]+)/$', views.PostListByCategoryView.as_view(), name='list_category'),
    # ex: /posts/post-title-0/
    url(r'^(?P<slug>[-\w]+)/$', views.PostDetailView.as_view(), name='details'),
    # ex: /posts/1/
    url(r'^(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='details'),
]

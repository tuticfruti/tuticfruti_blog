# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /posts/
    url(r'^$', views.PostListView.as_view(), name='list'),

    # ex: /posts/post-title-0/
    url(r'^(?P<slug>(?!search)[-\w]+)/$', views.PostDetailView.as_view(), name='detail'),

    # ex: /posts/id/1/
    url(r'^id/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail_by_pk'),

    # ex: /posts/category/python/
    url(r'^category/(?P<category_id>[a-z]+)/$', views.PostListByCategoryView.as_view(), name='list_by_category'),

    # ex: /posts/search/
    url(r'^search/$', views.PostListSearchView.as_view(), name='search'),
    # ex: /posts/category/python/search/
    url(
        r'^(?P<category_id>[a-z]+)/search/$',
        views.PostListSearchView.as_view(),
        name='search_by_category'),
]

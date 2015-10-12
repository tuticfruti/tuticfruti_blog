# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /posts/
    url(r'^$', views.PostListView.as_view(), name='list'),

    # ex: /posts/post/post-title-0/
    url(r'^post/(?P<slug>(?!search)[-\w]+)/$', views.PostDetailView.as_view(), name='detail'),

    # ex: /posts/post/1/
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetailView.as_view(), name='detail_by_pk'),

    # ex: /posts/category/python/
    url(r'^category/(?P<slug>[-\w]+)/$', views.PostListByCategoryView.as_view(), name='list_by_category'),

    # ex: /posts/search/
    url(r'^search/$', views.PostListSearchView.as_view(), name='search'),
    # ex: /posts/category/python/search/
    url(
        r'^category/(?P<slug>[-\w]+)/search/$',
        views.PostListSearchView.as_view(),
        name='search_by_category'),
]

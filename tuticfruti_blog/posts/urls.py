# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r'^search/$',
        view=views.PostListView.as_view(),
        name='search',
    ),
    url(
        regex=r'^(?P<category_id>[a-z]+)/search/$',
        view=views.PostListView.as_view(),
        name='search_category',
    ),
    url(
        regex=r'^(?P<category_id>[a-z]+)/$',
        view=views.PostListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^(?P<slug>[a-zA-Z-]+)/$',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
]

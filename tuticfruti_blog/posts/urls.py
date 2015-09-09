# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views
from .models import Post

urlpatterns = [
    url(
        regex=r'^category/(?P<category_id>[a-z]+)/$',
        view=views.PostListView.as_view(),
        name='list',
    ),
    url(
        regex=r'^(?P<slug>[a-zA-Z-]+)/$',
        view=views.PostDetailView.as_view(),
        name='detail'
    ),
]

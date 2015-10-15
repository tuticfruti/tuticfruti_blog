# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from tuticfruti_blog.posts import views

urlpatterns = [
    url(r'^$', views.PostListView.as_view(), name="home"),

    # Django Admin
    url(r'^admin/', include(admin.site.urls)),

    # Your stuff: custom urls includes go here
    #CKEditor
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    # User management
    url(_(r'^users/'), include("tuticfruti_blog.users.urls", namespace="users")),
    url(_(r'^accounts/'), include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(_(r'^posts/'), include('tuticfruti_blog.posts.urls', namespace='posts')), )

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', 'django.views.defaults.bad_request'),
        url(r'^403/$', 'django.views.defaults.permission_denied'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
        url(r'^500/$', 'django.views.defaults.server_error'),
    ]

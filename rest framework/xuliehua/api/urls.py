# author navigator
from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    re_path('^(?P<version>[v1|v2]+)/use/$', views.UseView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/use/(?P<pk>\d+)/$', views.UseView.as_view()),
    re_path('^books/$',views.Book.as_view()),
    re_path('^books/(?P<pk>\d+)/$',views.Book.as_view()),
]
# author navigator
from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'xxx',views.V1View)

app_name = 'api'
urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path('^(?P<version>[v1|v2]+)/users-(?P<id>\d+)/$', views.UsersView.as_view(),name="use"),
    re_path('^(?P<version>[v1|v2]+)/info/$', views.UserInfo.as_view()),
    re_path('^(?P<version>[v1|v2]+)/order/$', views.Order.as_view()),
    re_path('^(?P<version>[v1|v2]+)/Page/$', views.PageView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/v1/$', views.V1View.as_view({'get':'list','post':'create'})),
    re_path(r'^(?P<version>[v1|v2]+)/',include(router.urls)),
    re_path('^(?P<version>[v1|v2]+)/test/$', views.TestView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/use/$', views.UseView.as_view()),
    re_path('^(?P<version>[v1|v2]+)/use-(?P<pk>\d+)/$', views.UseView.as_view()),
]
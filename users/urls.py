# -*- coding: utf-8 -*-
# @Time    : 17-9-5 下午4:39
# @Author  : Wang Chao
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login/$', views.acc_login, name="login"),
    url(r'^log_out/$', views.log_out, name="log_out"),
]

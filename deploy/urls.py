#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import url, include
from django.contrib import admin
from deploy import views

urlpatterns = [
    url(r'^batchcmd/$', views.batchcmd, name="batch_cmd"),
    url(r'^salt_list/$', views.salt_list, name="salt_list"),
    url(r'^code_distribution/$', views.code_distribution, name="code_distribution"),
    url(r'^key_delete/$', views.key_delete, name="key_delete"),
    url(r'^key_accept/$', views.key_accept, name="key_accept"),
    url(r'^module_deploy/$', views.module_deploy, name="module_deploy"),

    # url(r'^$',views.index,name="index"),
]

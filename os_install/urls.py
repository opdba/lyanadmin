#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls import  url,include
from django.contrib import admin
from os_install import views
urlpatterns = [
    url(r'^install_list/$',views.install_list,name = "install_list"),

    #url(r'^$',views.index,name="index"),
]
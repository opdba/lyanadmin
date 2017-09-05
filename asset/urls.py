# -*- coding: utf-8 -*-
# @Time    : 17-9-5 下午4:48
# @Author  : Wang Chao
from django.conf.urls import url, include
from asset import views

urlpatterns = [
    url(r'^asset_report/$', views.asset_report),
    url(r'^asset_report_no_id/$', views.asset_report_no_id),
    url(r'^$', views.index, name="index"),
    url(r'^asset_list/$', views.asset_list, name="asset_list"),
    url(r'^get_asset_list/$', views.get_asset_list, name="get_asset_list"),
    url(r'^asset_list/(\d+)/$', views.asset_detail, name="asset_detail"),
    url(r'^event_log_list/$', views.event_log_list, name="event_log_list"),
    # url(r'^asset_event_logs/(\d+)/$',views.asset_event_logs,name="asset_event_logs" ),
    url(r'^asset_event_logs/$', views.asset_event_logs, name="asset_event_logs"),
    url(r'^approval/$', views.assets_approval, name="assets_approval"),
    url(r'^new_assets_approval/$', views.new_assets_approval, name="new_assets_approval"),
    url(r'^get_new_assets_approval/$', views.get_new_assets_approval, name="get_new_assets_approval"),
    url(r'^asset_compile/$', views.asset_compile, name="asset_compile"),
    url(r'^asset_create/$', views.asset_create, name="asset_create"),
    url(r'^asset_delete/$', views.asset_delete, name="asset_delete"),
    url(r'^asset_linkman/$', views.asset_linkman, name="asset_linkman"),
    url(r'^get_asset_linkman/$', views.get_asset_linkman, name="get_asset_linkman"),
    url(r'^error/$', views.error_403, name="error_403"),
    url(r'^error2/$', views.error_404, name="error_404"),
    url(r'^btn_create/$', views.btn_create, name="btn_create"),
    url(r'^btn_update/$', views.btn_update, name="btn_update"),
    url(r'^project_list/$', views.project_list, name="project_list"),
    url(r'^business_list/$', views.business_list, name="business_list"),
    url(r'^project_create/$', views.project_create, name="project_create"),
    url(r'^project_compile/$', views.project_compile, name="project_compile"),
    url(r'^project_delete/$', views.project_delete, name="project_delete"),
    url(r'^business_create/$', views.business_create, name="business_create"),
    url(r'^business_compile/$', views.business_compile, name="business_compile"),
    url(r'^business_delete/$', views.business_delete, name="business_delete"),

]

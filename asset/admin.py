# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from asset import models
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect


class ServerInline(admin.TabularInline):
    model = models.Server
    exclude = ('memo',)  # 不显示谁
    readonly_fields = ['create_date']  # 哪个不能改


class CPUInline(admin.TabularInline):
    model = models.CPU
    exclude = ('memo',)
    readonly_fields = ['create_date']


class NICInline(admin.TabularInline):
    model = models.NIC
    exclude = ('memo',)
    readonly_fields = ['create_date']


class RAMInline(admin.TabularInline):
    model = models.RAM
    exclude = ('memo',)
    readonly_fields = ['create_date']


class DiskInline(admin.TabularInline):
    model = models.Disk
    exclude = ('memo',)
    readonly_fields = ['create_date']


class AssetAdmin(admin.ModelAdmin):
    list_display = ('id', 'asset_type', 'sn', 'name', 'management_ip')
    inlines = [ServerInline, ]
    search_fields = ['sn', ]
    list_filter = ['asset_type']


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.IDC)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC)
admin.site.register(models.RAM)
admin.site.register(models.EventLog)
admin.site.register(models.Permission)
admin.site.register(models.Projectname)
admin.site.register(models.Application)

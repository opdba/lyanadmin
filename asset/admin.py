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
    list_display = ('id', 'asset_type', 'sn', 'name', 'manufactory', 'management_ip')
    inlines = [ServerInline, CPUInline, RAMInline, DiskInline, NICInline]
    search_fields = ['sn', ]
    list_filter = ['manufactory', 'asset_type']


class NicAdmin(admin.ModelAdmin):
    list_display = ('name', 'macaddress', 'ipaddress', 'netmask', 'bonding')
    search_fields = ('macaddress', 'ipaddress')


class NewAssetApprovalZoneAdmin(admin.ModelAdmin):
    list_display = ('sn', 'asset_type', 'manufactory', 'model', 'cpu_model', 'cpu_count', 'cpu_core_count', 'ram_size',
                    'os_distribution', 'os_release', 'date', 'approved', 'approved_by', 'approved_date')
    actions = ['approve_selected_objects']

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    approve_selected_objects.short_description = "批准入库"


admin.site.register(models.Asset, AssetAdmin)
admin.site.register(models.Server)
admin.site.register(models.NetworkDevice)
admin.site.register(models.IDC)
admin.site.register(models.Contract)
admin.site.register(models.CPU)
admin.site.register(models.Disk)
admin.site.register(models.NIC, NicAdmin)
admin.site.register(models.RAM)
admin.site.register(models.Manufactory)
admin.site.register(models.Software)
admin.site.register(models.EventLog)
admin.site.register(models.NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Permission)
admin.site.register(models.Projectname)
admin.site.register(models.Application)
admin.site.register(models.Linkman)

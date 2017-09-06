# -*-coding:utf8-*-
from __future__ import unicode_literals
from django.db import models
from users.models import User


# Create your models here.

class Asset(models.Model):
    asset_type_choice = (('server', u'服务器'),
                         ('switch', u'交换机'),
                         ('router', u'路由器'),
                         ('firewall', u'防火墙'),
                         ('others', u'其他类'),)
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server')
    name = models.CharField(u'序列号', max_length=64, unique=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True, null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True)
    idc_jg = models.CharField(max_length=10, verbose_name=u'机柜编号', null=True, blank=True)
    status_type = (
        (1, u'在用'),
        (2, u'停用'),)
    status = models.IntegerField(choices=status_type, default=1, verbose_name=u'使用状态', null=True, blank=True)
    projectname = models.ForeignKey('Projectname', verbose_name=u'项目名称', null=True, blank=True)
    application = models.ForeignKey('Application', verbose_name=u'业务名称', null=True, blank=True)
    module = models.CharField(u'模块', max_length=64, null=True, blank=True)
    trade_date = models.DateField(u'购买时间', null=True, blank=True)
    expire_date = models.DateField(u'过保修期', null=True, blank=True)
    price = models.FloatField(u'价格', null=True, blank=True)
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'

    def __unicode__(self):
        return 'id:%s name:%s' % (self.id, self.name)


class Projectname(models.Model):  # 项目名称
    name = models.CharField(u'项目名称', max_length=64, unique=True)
    memo = models.TextField(u'备注', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '项目名称'
        verbose_name_plural = '项目名称'


class Application(models.Model):  # 业务名称
    name = models.CharField(u'业务名称', max_length=64, unique=True)
    memo = models.TextField(u'备注', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '业务名称'
        verbose_name_plural = '业务名称'


class IDC(models.Model):
    name = models.CharField(u'机房名称', max_length=64, unique=True)
    idc_type = models.CharField(u'机房类型', max_length=20, null=True, blank=True)
    idc_location = models.CharField(u'机房位置', max_length=30, null=True, blank=True)
    idc_contacts = models.CharField(u'联系电话', max_length=30, null=True, blank=True)
    memo = models.TextField(u'备注', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'


class Server(models.Model):
    asset = models.OneToOneField('Asset')
    created_by_choices = (('auto', 'Auto'),  # 自动创建
                          ('manual', 'Manual'))  # 手动创建
    created_by = models.CharField(choices=created_by_choices, max_length=32, default='auto')
    hosted_on = models.ForeignKey('Server', related_name='host_on_server', null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    raid_type = models.CharField(u'raid类型', max_length=512, null=True, blank=True)
    os_type = models.CharField(u'操作系统类型', max_length=64, blank=True, null=True)
    os_distribution = models.CharField(u'发型版本', max_length=64, blank=True, null=True)
    os_release = models.CharField(u'操作系统版本', max_length=64, blank=True, null=True)

    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"

    def __unicode__(self):
        return self.os_type


class EventLog(models.Model):
    name = models.CharField(u'事件名称', max_length=100)
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
        (7, u'IDC信息'),
    )
    event_type = models.SmallIntegerField(u'事件类型', choices=event_type_choices)
    # asset = models.ForeignKey('Asset')
    component = models.CharField('事件子项', max_length=255, blank=True, null=True)
    detail = models.TextField(u'事件详情')
    date = models.DateTimeField(u'事件时间', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name=u'事件源')
    memo = models.TextField(u'备注', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '事件纪录'
        verbose_name_plural = "事件纪录"


class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def __unicode__(self):
        return self.cpu_core_count


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s:%s' % (self.asset_id,  self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SSD', 'SSD'),
    )
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __unicode__(self):
        return '%s: capacity:%s' % (self.asset_id, self.capacity)


class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']


class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True)
    describe = models.CharField('描述', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '权限表'
        verbose_name_plural = verbose_name
        # 权限信息，这里定义的权限的名字，后面是描述信息，描述信息是在django admin中显示权限用的

        permissions = (
            ("view_asset_create", u"创建资产"),
            ("view_asset_compile", u"编辑资产"),
            ("view_asset_delete", u"删除资产"),
            ("btn_asset_create", u"创建按钮"),
            ("btn_asset_compile", u"编辑按钮"),
            ("btn_asset_delete", u"删除按钮"),

        )

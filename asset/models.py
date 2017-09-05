# -*-coding:utf8-*-
from __future__ import unicode_literals
from django.db import models
from users.models import User


# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(u'姓名', max_length=64, blank=True, null=True)
    token = models.CharField(u'token', max_length=128, default=None, blank=True, null=True)
    department = models.CharField(u'部门', max_length=32, default=None, blank=True, null=True)
    tel = models.CharField(u'座机', max_length=32, default=None, blank=True, null=True)
    mobile = models.CharField(u'手机', max_length=32, default=None, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True, default=None)
    valid_begin_time = models.DateTimeField(auto_now_add=True)
    valid_end_time = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'用户列表'
        verbose_name_plural = u'用户列表'


class Asset(models.Model):
    asset_type_choice = (('server', u'服务器'),
                         ('switch', u'交换机'),
                         ('router', u'路由器'),
                         ('firewall', u'防火墙'),
                         ('storage', u'存储设备'),
                         ('NLB', u'NetScaler'),
                         ('wireless', u'无线AP'),
                         ('software', u'软件资产'),
                         ('others', u'其他类'),)
    asset_type = models.CharField(choices=asset_type_choice, max_length=64, default='server')
    name = models.CharField(u'序列号', max_length=64, unique=True)
    sn = models.CharField(u'资产SN号', max_length=128, unique=True, null=True, blank=True)
    manufactory = models.ForeignKey('Manufactory', verbose_name=u'制造商', null=True, blank=True)
    management_ip = models.GenericIPAddressField(u'管理IP', blank=True, null=True)
    idc = models.ForeignKey('IDC', verbose_name=u'IDC机房', null=True, blank=True)
    idc_jg = models.CharField(max_length=10, verbose_name=u'机柜编号', null=True, blank=True)
    status_type = (
        (1, u'在用'),
        (2, u'停用'),)
    status = models.IntegerField(choices=status_type, default=1, verbose_name=u'使用状态', null=True, blank=True)
    admin = models.ForeignKey('UserProfile', verbose_name=u'资产管理员', null=True, blank=True, default=1)
    linkman = models.ForeignKey('Linkman', verbose_name=u'联系人', null=True, blank=True)
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


class Linkman(models.Model):
    name = models.CharField(u'姓名', max_length=64, unique=True)
    phone = models.IntegerField(u'手机', null=True, blank=True)
    fixed_phone = models.IntegerField(u'座机', null=True, blank=True)
    department = models.CharField(u'部门', max_length=64, null=True, blank=True)
    email = models.CharField(u'邮箱', max_length=64, null=True, blank=True)
    qq = models.CharField(u'QQ', max_length=64, null=True, blank=True)
    memo = models.TextField(u'备注', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = u'联系人列表'
        verbose_name_plural = u'联系人列表'

    def __unicode__(self):
        return self.name


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


class Manufactory(models.Model):  # 厂商
    manufactory = models.CharField(u'厂商名称', max_length=64, unique=True)
    support_num = models.CharField(u'支持电话', max_length=32, blank=True)
    memo = models.TextField(u'备注', max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.manufactory

    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'


class Contract(models.Model):  # 合同
    contract_number = models.CharField(u'合同号', max_length=128, unique=True)
    name = models.CharField(u' 合同名称', max_length=64)
    memo = models.TextField(u'备注', null=True, blank=True)
    price = models.IntegerField(u'合同金额')
    detile = models.TextField(u'合同明细', blank=True, null=True)
    start_date = models.DateField(blank=True)
    end_date = models.DateField(blank=True)
    license_num = models.IntegerField(u'license数量', blank=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, auto_now=True)

    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'

    def __unicode__(self):
        return self.name


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


class NetworkDevice(models.Model):
    asset = models.OneToOneField('Asset')
    vlan_ip = models.GenericIPAddressField(u'VlanIP', blank=True, null=True)
    intranet_ip = models.GenericIPAddressField(u'内网IP', blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, null=True, blank=True)
    model = models.CharField(u'型号', max_length=128, null=True, blank=True)
    firmware = models.ForeignKey('Software', blank=True, null=True)
    port_num = models.SmallIntegerField(u'端口个数', null=True, blank=True)
    device_detail = models.TextField(u'设置详细配置', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = "网络设备"


class Software(models.Model):
    os_types_choice = (
        ('linux', 'Linux'),
        ('windows', 'Windows'),
        ('network_firmware', 'Network Firmware'),
        ('software', 'Softwares'),
    )
    os_distribution_choices = (('windows', 'Windows'),
                               ('centos', 'CentOS'),
                               ('ubuntu', 'Ubuntu'))
    type = models.CharField(u'系统类型', choices=os_types_choice, max_length=64, help_text=u'eg. GNU/Linux', default=1)
    distribution = models.CharField(u'发型版本', choices=os_distribution_choices, max_length=32, default='windows')
    version = models.CharField(u'软件/系统版本', max_length=64, help_text=u'eg. CentOS release 6.5 (Final)', unique=True)
    language_choices = (('cn', u'中文'),
                        ('en', u'英文'))
    language = models.CharField(u'系统语言', choices=language_choices, default='cn', max_length=32)

    # version = models.CharField(u'版本号', max_length=64,help_text=u'2.6.32-431.3.1.el6.x86_64' )

    def __unicode__(self):
        return self.version

    class Meta:
        verbose_name = '软件/系统'
        verbose_name_plural = "软件/系统"


class CPU(models.Model):
    asset = models.OneToOneField('Asset')
    cpu_model = models.CharField(u'CPU型号', max_length=128, blank=True)
    cpu_count = models.SmallIntegerField(u'物理cpu个数')
    cpu_core_count = models.SmallIntegerField(u'cpu核数')
    memo = models.TextField(u'备注', null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = "CPU部件"

    def __unicode__(self):
        return self.cpu_model


class RAM(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'内存型号', max_length=128)
    slot = models.CharField(u'插槽', max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    capacity = models.IntegerField(u'内存大小(MB)')
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s:%s:%s' % (self.asset_id, self.slot, self.capacity)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = "RAM"
        unique_together = ("asset", "slot")  # 联合唯一

    auto_create_fields = ['sn', 'slot', 'model', 'capacity']


class Disk(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插槽位', max_length=64)
    manufactory = models.CharField(u'制造商', max_length=64, blank=True, null=True)
    model = models.CharField(u'磁盘型号', max_length=128, blank=True, null=True)
    capacity = models.FloatField(u'磁盘容量GB')
    disk_iface_choice = (
        ('SATA', 'SATA'),
        ('SAS', 'SAS'),
        ('SCSI', 'SCSI'),
        ('SSD', 'SSD'),
    )

    iface_type = models.CharField(u'接口类型', max_length=64, choices=disk_iface_choice, default='SAS')
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    # auto_create_fields = ['sn','slot','manufactory','model','capacity','iface_type']
    class Meta:
        unique_together = ("asset", "slot")
        verbose_name = '硬盘'
        verbose_name_plural = "硬盘"

    def __unicode__(self):
        return '%s:slot:%s capacity:%s' % (self.asset_id, self.slot, self.capacity)


class NIC(models.Model):
    asset = models.ForeignKey('Asset')
    name = models.CharField(u'网卡名', max_length=64, blank=True, null=True)
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    model = models.CharField(u'网卡型号', max_length=128, blank=True, null=True)
    macaddress = models.CharField(u'MAC', max_length=64, unique=True)
    ipaddress = models.GenericIPAddressField(u'IP', blank=True, null=True)
    netmask = models.CharField(max_length=64, blank=True, null=True)
    bonding = models.CharField(max_length=64, blank=True, null=True)
    memo = models.CharField(u'备注', max_length=128, blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return '%s:%s' % (self.asset_id, self.macaddress)

    class Meta:
        verbose_name = u'网卡'
        verbose_name_plural = u"网卡"

    auto_create_fields = ['name', 'sn', 'model', 'macaddress', 'ipaddress', 'netmask', 'bonding']


class RaidAdaptor(models.Model):
    asset = models.ForeignKey('Asset')
    sn = models.CharField(u'SN号', max_length=128, blank=True, null=True)
    slot = models.CharField(u'插口', max_length=64)
    model = models.CharField(u'型号', max_length=64, blank=True, null=True)
    memo = models.TextField(u'备注', blank=True, null=True)
    create_date = models.DateTimeField(blank=True, auto_now_add=True)
    update_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return self.asset.name

    class Meta:
        unique_together = ("asset", "slot")


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


class NewAssetApprovalZone(models.Model):
    sn = models.CharField(u'资产SN号', max_length=128, unique=True)
    asset_type_choices = (
        ('server', u'服务器'),
        ('switch', u'交换机'),
        ('router', u'路由器'),
        ('firewall', u'防火墙'),
        ('storage', u'存储设备'),
        ('NLB', u'NetScaler'),
        ('wireless', u'无线AP'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    manufactory = models.CharField(max_length=64, blank=True, null=True)
    model = models.CharField(max_length=128, blank=True, null=True)
    ram_size = models.IntegerField(blank=True, null=True)
    cpu_model = models.CharField(max_length=128, blank=True, null=True)
    cpu_count = models.IntegerField(blank=True, null=True)
    cpu_core_count = models.IntegerField(blank=True, null=True)
    os_distribution = models.CharField(max_length=64, blank=True, null=True)
    os_type = models.CharField(max_length=64, blank=True, null=True)
    os_release = models.CharField(max_length=64, blank=True, null=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey('UserProfile', verbose_name=u'批准人', blank=True, null=True)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __unicode__(self):
        return self.sn

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"


class Permission(models.Model):
    name = models.CharField("权限名称", max_length=64)
    url = models.CharField('URL名称', max_length=255)
    chioces = ((1, 'GET'), (2, 'POST'))
    per_method = models.SmallIntegerField('请求方法', choices=chioces, default=1)
    argument_list = models.CharField('参数列表', max_length=255, help_text='多个参数之间用英文半角逗号隔开', blank=True, null=True)
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

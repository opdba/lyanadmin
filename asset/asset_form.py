# -*-coding:utf8-*-
from django import forms
from asset import models

class AssetForm(forms.Form):
    serial_name = forms.CharField(error_messages={"required": "序列号不能为空"},  # 设置显示的错误信息
                         widget=forms.TextInput(attrs={"class": "form-control",'id':'serial_name','readonly':'true',
                                                  }))
    asset_type_choice=(
         ('server', u'服务器'),
         ('switch', u'交换机'),
         ('router', u'路由器'),
         ('firewall', u'防火墙'),
         ('storage', u'存储设备'),
         ('NLB', u'NetScaler'),
         ('wireless', u'无线AP'),
         ('software', u'软件资产'),
         ('others', u'其他类'),
        )
    asset_type = forms.CharField(widget=forms.widgets.Select(choices=asset_type_choice,
                                                                      attrs={'class': "form-control selectpicker",'id':'asset_type'}))

    ip = forms.GenericIPAddressField(error_messages={"required": "ip不能为空"},
                         widget=forms.TextInput(attrs={"class": "form-control",'id':'ip',
                                                       "placeholder": "IP地址"}))  # 添加属性和样式

    idc_type = forms.IntegerField(widget=forms.widgets.Select(attrs={'class': "form-control selectpicker",'id':'idc_type'}))


    idc_jg = forms.CharField(error_messages={"required": "机柜编号不能为空"},
                             widget=forms.TextInput(attrs={"class": "form-control",'id':'idc_jg',
                                                           "placeholder": "机柜编号"}))

    projectname = forms.IntegerField(widget=forms.widgets.Select(
                attrs={'class': "form-control selectpicker show-tick", 'data-live-search': "true",'data-size':'5',
               'id': 'projectname'}))

    application = forms.IntegerField(widget=forms.widgets.Select(
        attrs={'class': "form-control selectpicker show-tick", 'data-live-search': "true",'data-size':'5',
               'id': 'application'}))

    module = forms.CharField(error_messages={"required": "模块"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'module',
                                                                "placeholder": "模块"}))
    status_type=(
         (1, '在用'),
         (2, '停用')
        )
    status = forms.IntegerField(widget=forms.widgets.Select(choices=status_type,
                                                                      attrs={'class': "form-control selectpicker",'id':'status'}))

    linkman_type = forms.IntegerField(widget=forms.widgets.Select(attrs={'class': "form-control selectpicker show-tick",'data-live-search':"true",'data-size':'5',
                                                                         'id':'linkman_type'}))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control",'id':'memo',
                                                        "placeholder": "备注"})  # 添加属性和样式
                           )

    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        data_tuple = models.IDC.objects.all().values_list('id', 'name')
        self.fields['idc_type'].widget.choices = data_tuple

        data_tuple1 = models.Linkman.objects.all().values_list('id', 'name')
        self.fields['linkman_type'].widget.choices = data_tuple1

        data_tuple1 = models.Projectname.objects.all().values_list('id', 'name')
        self.fields['projectname'].widget.choices = data_tuple1

        data_tuple1 = models.Application.objects.all().values_list('id', 'name')
        self.fields['application'].widget.choices = data_tuple1


class AssetForm_create(forms.Form):

    serial_name = forms.CharField(error_messages={"required": "序列号不能为空"},  # 设置显示的错误信息
                           widget=forms.TextInput(attrs={"class": "form-control", 'id': 'serial_name_create',
                                                         "placeholder": "序列号"}))
    asset_type_choice=(
         ('server', u'服务器'),
         ('switch', u'交换机'),
         ('router', u'路由器'),
         ('firewall', u'防火墙'),
         ('storage', u'存储设备'),
         ('NLB', u'NetScaler'),
         ('wireless', u'无线AP'),
         ('software', u'软件资产'),
         ('others', u'其他类'),
        )
    asset_type = forms.CharField(widget=forms.widgets.Select(choices=asset_type_choice,
                                                                      attrs={'class': "form-control selectpicker",'id':'asset_type_create'}))
    ip = forms.GenericIPAddressField(error_messages={"required": "ip不能为空"},
                         widget=forms.TextInput(attrs={"class": "form-control",'id':'ip_create',
                                                       "placeholder": "管理IP"}))  # 添加属性和样式
    idc_type = forms.IntegerField(widget=forms.widgets.Select(attrs={'class': "form-control selectpicker",'id':'idc_type_create'}))

    idc_jg = forms.CharField(error_messages={"required": "机柜编号不能为空"},
                             widget=forms.TextInput(attrs={"class": "form-control",'id':'idc_jg_create',
                                                           "placeholder": "机柜编号"}))
    projectname = forms.IntegerField(widget=forms.widgets.Select(
                attrs={'class': "form-control selectpicker show-tick", 'title': 'Nothing selected', 'data-live-search': "true",'data-size':'5',
               'id': 'projectname_create'}))

    application = forms.IntegerField(widget=forms.widgets.Select(
        attrs={'class': "form-control selectpicker show-tick", 'title': 'Nothing selected', 'data-live-search': "true",'data-size':'5',
               'id': 'application_create'}))

    module = forms.CharField(error_messages={"required": "模块"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'module_create',
                                                                "placeholder": "模块"}))
    status_type=(
         (1, '在用'),
         (2, '停用'),
        )
    status = forms.IntegerField(widget=forms.widgets.Select(choices=status_type,
                                                                      attrs={'class': "form-control selectpicker",'id':'status_create'}))

    linkman_type = forms.IntegerField(widget=forms.widgets.Select(attrs={'class': "form-control selectpicker show-tick",'title':'Nothing selected','data-size':'5',
                                                                         'data-live-search':"true",'id':'linkman_type_create'}))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control",'id':'memo_create',
                                                        "placeholder": "备注"})  # 添加属性和样式
                           )


    def __init__(self, *args, **kwargs):
        super(AssetForm_create, self).__init__(*args, **kwargs)
        data_tuple = models.IDC.objects.all().values_list('id', 'name')
        self.fields['idc_type'].widget.choices = data_tuple

        data_tuple1 = models.Linkman.objects.all().values_list('id', 'name')
        self.fields['linkman_type'].widget.choices = data_tuple1

        data_tuple1 = models.Projectname.objects.all().values_list('id', 'name')
        self.fields['projectname'].widget.choices = data_tuple1

        data_tuple1 = models.Application.objects.all().values_list('id', 'name')
        self.fields['application'].widget.choices = data_tuple1


class projectForm_create(forms.Form):
    project_name = forms.CharField(error_messages={"required": "项目名不能为空"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'project_name_create', }))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control", 'id': 'memo_create',"placeholder": "备注"}))

class projectForm_update(forms.Form):
    project_id = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control", 'id': 'id_update', 'readonly': 'true',}))
    project_name = forms.CharField(error_messages={"required": "项目名不能为空"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'project_name_update', }))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control", 'id': 'memo_update',"placeholder": "备注"}))


class businessForm_create(forms.Form):
    business_name = forms.CharField(error_messages={"required": "项目名不能为空"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'business_name_create', }))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control", 'id': 'memo_create',"placeholder": "备注"}))

class businessForm_update(forms.Form):
    business_id = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control", 'id': 'id_update', 'readonly': 'true',}))
    business_name = forms.CharField(error_messages={"required": "项目名不能为空"},  # 设置显示的错误信息
                                  widget=forms.TextInput(attrs={"class": "form-control", 'id': 'business_name_update', }))

    memo = forms.CharField(required=False,  # 可以为空
                           widget=forms.Textarea(attrs={"class": "form-control", 'id': 'memo_update',"placeholder": "备注"}))






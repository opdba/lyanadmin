# -*- coding: utf-8 -*-
# -*-coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from asset import core, asset_handle
import json
from asset.token_required import token_required
from asset import models
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from asset import asset_form
from asset.permissions import check_permission


@csrf_exempt
# @token_required
def asset_report_no_id(request):
    if request.method == 'POST':
        ass = core.Asset(request)
        result = ass.get_asset_id_by_sn()
        return HttpResponse(json.dumps(result))


@csrf_exempt
# @token_required
def asset_report(request):
    if request.method == 'POST':
        ass = core.Asset(request)
        if ass.data_is_valid():
            ass.data_into()
        return HttpResponse(json.dumps(ass.response))
    return HttpResponse("OK")


@login_required
def index(request):
    return redirect("/asset/asset_list/")


# 资产列表
@login_required
def asset_list(request):
    '''生成前端创建和编辑的form样式'''
    obj = asset_form.AssetForm()
    obj_create = asset_form.AssetForm_create()

    return render(request, "assets/assets.html", {'obj': obj, 'obj_create': obj_create})


@login_required
def get_asset_list(request):
    '''获取资产列表'''
    asset_dic = asset_handle.fetch_asset_list()
    print(asset_dic)
    return HttpResponse(json.dumps(asset_dic))


@login_required
def asset_detail(request, asset_id):
    '''获取资产详情'''
    if request.method == "GET":
        try:
            asset_obj = models.Asset.objects.get(id=asset_id)
        except ObjectDoesNotExist as e:
            return render(request, 'assets/asset_detail.html', {'error': e})
        return render(request, 'assets/asset_detail.html', {"asset_obj": asset_obj})


@login_required
def event_log_list(request):
    return render(request, "assets/event_log_list.html")


# @login_required
# def asset_event_logs(request,asset_id):
#     '''变更记录'''
#     print(asset_id)
#     if request.method == "GET":
#         log_list = asset_handle.fetch_asset_event_logs(asset_id)
#         return HttpResponse(json.dumps(log_list))

@login_required
def asset_event_logs(request):
    '''变更记录'''
    if request.method == "GET":
        log_list = asset_handle.fetch_asset_event_logs()
        return HttpResponse(json.dumps(log_list))


@login_required
@check_permission
def asset_compile(request):
    '''编辑'''
    request_obj = request.POST
    print "--------------", request_obj

    try:
        user_input_obj = asset_form.AssetForm(request_obj)
        if user_input_obj.is_valid():  # 验证用户输入是否合法
            # data = user_input_obj.clean()  # 合法，获取数据
            obj = asset_handle.LogicalProcess(request_obj)
            obj.modification(request.user.id)
        else:
            error_msg = user_input_obj.errors.as_json()  # 不合法，返回错误信息
            return HttpResponse(error_msg)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse("seccess")


@login_required
@check_permission
def asset_create(request):
    '''新建'''
    request_obj = request.POST

    try:
        user_input_obj = asset_form.AssetForm_create(request_obj)
        print user_input_obj
        if user_input_obj.is_valid():  # 验证用户输入是否合法
            # data = user_input_obj.clean()  # 合法，获取数据
            obj = asset_handle.LogicalProcess(request_obj)
            obj.asset_create(request.user.id)
        else:
            error_msg = user_input_obj.errors.as_json()  # 不合法，返回错误信息
            return HttpResponse(error_msg)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse('seccess')


@login_required
@check_permission
def asset_delete(request):
    '''删除'''
    request_obj = request.POST
    try:
        obj = asset_handle.LogicalProcess(request_obj)
        obj.asset_delete(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse("list(" + json.dumps({"seccess": "seccess"}) + ")")


@login_required
def error_403(request):
    return render(request, 'assets/403.html')


@login_required
def error_404(request):
    return render(request, 'assets/404.html')


@login_required
@check_permission
def btn_create(request):
    '''创建按钮权限判断'''
    return HttpResponse("list(" + json.dumps({"aa": "seccess"}) + ")")


@login_required
@check_permission
def btn_update(request):
    '''编辑按钮权限判断'''
    return HttpResponse("list(" + json.dumps({"aa": "seccess"}) + ")")


@login_required
def project_list(request):
    if request.method == 'POST':
        project_list = asset_handle.fetch_project_list()
        print(project_list)
        return HttpResponse(json.dumps(project_list))
    else:

        obj_create = asset_form.projectForm_create()
        obj_update = asset_form.projectForm_update()
        return render(request, 'assets/project_list.html', {"obj_create": obj_create, "obj_update": obj_update})


@login_required
def project_create(request):
    '''项目创建'''
    request_obj = request.POST
    try:
        obj = asset_handle.ProjectLogical(request_obj)
        obj.Project_create(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse('seccess')


@login_required
def project_compile(request):
    '''项目编辑'''
    request_obj = request.POST
    print "asa", request_obj
    try:
        obj = asset_handle.ProjectLogical(request_obj)
        obj.modification(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse('seccess')


@login_required
def project_delete(request):
    '''项目删除'''
    request_obj = request.POST
    try:
        obj = asset_handle.ProjectLogical(request_obj)
        obj.Project_delete(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse("list(" + json.dumps({"seccess": "seccess"}) + ")")


@login_required
def business_list(request):
    if request.method == 'POST':
        business_list = asset_handle.fetch_business_list()
        print(business_list)
        return HttpResponse(json.dumps(business_list))
    else:
        obj_create = asset_form.businessForm_create()
        obj_update = asset_form.businessForm_update()
        return render(request, 'assets/business_list.html', {"obj_create": obj_create, "obj_update": obj_update})


@login_required
def business_create(request):
    '''业务创建'''
    request_obj = request.POST
    print request_obj
    try:
        obj = asset_handle.BusinessLogical(request_obj)
        obj.business_create(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse('seccess')


@login_required
def business_compile(request):
    '''业务编辑'''
    request_obj = request.POST
    try:
        obj = asset_handle.BusinessLogical(request_obj)
        obj.modification(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse('seccess')


@login_required
def business_delete(request):
    '''业务删除'''
    request_obj = request.POST
    try:
        obj = asset_handle.BusinessLogical(request_obj)
        obj.business_delete(request.user.id)
    except Exception as e:
        print e
        return HttpResponse(e)
    return HttpResponse("list(" + json.dumps({"seccess": "seccess"}) + ")")

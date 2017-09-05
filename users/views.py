# -*- coding: utf-8 -*-
# -*- coding:utf-8 -*-
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
import json


def acc_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session.set_expiry(0)  # 关闭浏览器session失效
            return redirect('/asset/asset_list/')
        else:
            return render(request, 'login.html', {'login_err': '用户名或密码错误!'})
    return render(request, "login.html")


def log_out(request):
    auth.logout(request)
    return redirect("/users/login/")


def home_page(request):
    return redirect("/asset/")


# 饼图
def test(request):
    data = [['已用:90%', 90.0], ['可用:10%', 10.0]]
    data = json.dumps(data)
    print(data)
    return HttpResponse(data)

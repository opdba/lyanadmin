#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import HttpResponse
import json


#饼图
def test(request):
    data = [['已用:90%', 90.0],['可用:10%',   10.0]]
    data = json.dumps(data)
    print(data)
    return HttpResponse(data)
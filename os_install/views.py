# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
def install_list(request):
    return render(request, 'os_install/install_list.html')

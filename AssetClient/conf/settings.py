#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
BaseDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Params = {
    "server": "172.16.8.62",
    "port":8666,
    'request_timeout':30,
    "urls":{
          "asset_report_no_id":"/asset/asset_report_no_id/",
          "asset_report":"/asset/asset_report/",
        },
    'asset_id_path':'%s/var/.asset_id' % BaseDir,
    'log_file': '%s/logs/run_log' % BaseDir,
    'auth':{
        'user':'851194999@qq.com',
        'token': 'abc'
        },

    'name' : ''
}
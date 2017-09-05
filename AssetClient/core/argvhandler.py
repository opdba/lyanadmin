#!/usr/bin/env python
# -*- coding:utf-8 -*-
from core import collect_info,api_token
from conf import settings
import datetime
import json
import os,sys,urllib,urllib2
class ArgvHandler(object):
    def __init__(self,argv):
        self.argv = argv
        self.parse_argv()

    def parse_argv(self):
        if len(self.argv) > 1:
            print(self.argv[1])
            if hasattr(self,self.argv[1]):
                func = getattr(self,self.argv[1])
                func()
            else:
                self.help_msg()
        else:
            self.help_msg()

    def help_msg(self):
        msg = '''
            collect_data    收集信息
            report_asset    报告资产
        '''
        print(msg)

    def collect_data(self):
        obj = collect_info.Collect_Info()
        asset_data = obj.collect()
        print("返回收集信息")
        print(asset_data) #返回的大字典

    def report_asset(self):
        obj = collect_info.Collect_Info()
        asset_data = obj.collect()
        #print(aasset_data) #返回的大字典
        asset_id = self.obtain_asset_id(asset_data['sn'])

        if asset_id:    #如果有资产id
            asset_data["asset_id"] = asset_id
            post_url = "asset_report"
        else:
            asset_data["asset_id"] = None
            post_url = "asset_report_no_id"

        data = {"asset_data": json.dumps(asset_data)}
        response = self.__submit_data(post_url,data,method="post")#发起请求

        if "asset_id" in response:
            self.__update_asset_id(response["asset_id"])
        self.log_record(response)

    def __update_asset_id(self,new_asset_id):
        asset_id_file = settings.Params['asset_id_path']
        f = open(asset_id_file,"wb")
        f.write(str(new_asset_id))
        f.close()


    def obtain_asset_id(self,sn=None):
        asset_id_file = settings.Params['asset_id_path']
        if os.path.isfile(asset_id_file):
            asset_id = open(asset_id_file).read().strip()
            if asset_id.isdigit():
                return  asset_id

    def __attach_token(self,url_str):
        '''生成一个加密验证在url后'''
        user = settings.Params['auth']['user']
        token_id = settings.Params['auth']['token']

        md5_token,timestamp = api_token.get_token(user,token_id)
        url_arg_str = "user=%s&timestamp=%s&token=%s" %(user,timestamp,md5_token)
        if "?" in url_str:#already has arg
            new_url = url_str + "&" + url_arg_str
        else:
            new_url = url_str + "?" + url_arg_str
        return  new_url

    def __submit_data(self,post_url,asset_data,method):
        if post_url in settings.Params['urls']:
            if type(settings.Params['port']) is int:
                url = "http://%s:%s%s" %(settings.Params['server'],settings.Params['port'],settings.Params['urls'][post_url])
            else:
                url = "http://%s%s" %(settings.Params['server'],settings.Params['urls'][post_url])

            url = self.__attach_token(url)
            if method == 'post':
                print(url)
                try:
                    data_encode = urllib.urlencode(asset_data)
                    req = urllib2.Request(url=url,data=data_encode)
                    res_data = urllib2.urlopen(req,timeout=settings.Params['request_timeout'])
                    callback = res_data.read()
                    callback = json.loads(callback)
                    print ("\033[31;1m[%s]:[%s]\033[0m response:\n%s" %(method,url,callback))

                    return callback
                except Exception as e:
                    sys.exit("\033[31;1m%s\033[0m"%e)

    def log_record(self,log,action_type=None):
        f = file(settings.Params["log_file"],"ab")
        if log is str:
            pass
        if type(log) is dict:

            if "info" in log:
                for msg in log["info"]:
                    log_format = "%s\tINFO\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    #print msg
                    f.write(log_format)
            if "error" in log:
                for msg in log["error"]:
                    log_format = "%s\tERROR\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
            if "warning" in log:
                for msg in log["warning"]:
                    log_format = "%s\tWARNING\t%s\n" %(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),msg)
                    f.write(log_format)
        f.close()






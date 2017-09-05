# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from lyanadmin import settings
from deploy.api.saltapi2 import SaltAPI
from code_pub import Code_Work
from build_data import BuildData
import time
from deploy import models
from asset import models as asset_models
def batchcmd(request):
    '''命令执行'''
    if request.method == 'POST':
        tgt = request.POST.get('tgt')
        arg = request.POST.get('arg')

        sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])

        params = {'client':'local', 'fun':'cmd.run', 'tgt':tgt,'arg':arg}
        result = sapi.saltCmd(params)
        print(result)
        return render(request,"deploy/batch_cmd.html",{'result':result})
    else:
        return render(request,"deploy/batch_cmd.html")

def salt_list(request):
    """所有key"""
    #user = request.user
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    minions,minions_pre = sapi.list_all_key()

    return render(request,'deploy/salt_key_list.html', {'all_minions': minions, 'all_minions_pre': minions_pre})

def key_accept(request):
    '''允许key'''
    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    ret = sapi.accept_key(node_name)
    models.Message.objects.create(type='salt', action='accept_key', action_ip=node_name, content='saltstack 接收key')
    return HttpResponseRedirect('/deploy/salt_list/')

def key_delete(request):
    '''删除key'''
    node_name = request.GET.get('node_name')
    sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
    ret = sapi.delete_key(node_name)

    models.Message.objects.create(type='salt', action='delete_key', action_ip=node_name, content='saltstack 删除key')
    return HttpResponseRedirect('/deploy/salt_list/')

def module_deploy(request):
    '''模块部署'''
    ret = ''
    if request.method == 'POST':
        print (request.POST)
        print (request.GET)
        ret = []
        action = request.GET.get('action')
        if action == 'deploy':
            tgt = request.POST.get('tgt')
            arg = request.POST.getlist('module')
            tgtcheck = asset_models.NIC.objects.filter(ipaddress=tgt)
            print(tgt,arg,tgtcheck)
            if tgtcheck:
                models.Message.objects.create(type='salt', action='deploy', action_ip=tgt, content='saltstack %s 模块部署' % (arg)) #写入日志
                sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                if 'sysinit' in arg:
                    obj = sapi.async_deploy(tgt,arg[-1])    #先执行初始化模块,其他任意
                    ret.append(obj)
                    arg.remove('sysinit')
                    if arg:
                        for i in arg:
                            obj = sapi.async_deploy(tgt,i)
                            ret.append(obj)
                else:
                    for i in arg:
                        obj = sapi.async_deploy(tgt,i)
                        ret.append(obj)

                #sapi.async_deploy('test-01','zabbix.api')   #调用zabbix.api执行模块监控
        else:
           ret = '目标主机不正确，请重新输入'
    return render(request,'deploy/salt_module_deploy.html', {'ret': ret})

#////////////
def code_distribution(request):
    """构建代码推送到服务器"""
    ret = ''
    host = {'ga': 'test-01', 'beta': 'localhost.localdomain'}
    user = request.user
    if request.method == 'POST':
        action = request.GET.get('action')

        if action == 'push':
            pro = request.POST.get('project')
            url = request.POST.get('url')
            version = request.POST.get('version')
            env = request.POST.get('env')
            print(pro,url,version,env)
            capi = Code_Work(pro=pro,url=url,ver=version)
            data = {pro:{'ver':version}}
            obj = capi.work()      #构建rpm包

            if obj['comment'][0]['result'] and obj['comment'][1]['result'] and obj['comment'][2]['result']:
                json_api = BuildData()
                json_api.build_data(host[env],data)   #刷新pillar数据，通过deploy下发SLS执行代码发布
                sapi = SaltAPI(url=settings.SALT_API['url'],username=settings.SALT_API['user'],password=settings.SALT_API['password'])
                if env == 'beta':
                    jid = sapi.target_deploy('beta','deploy.'+pro)
                elif env == 'ga':
                    jid = sapi.target_deploy('tg','deploy.'+pro)
                else:
                    jid = sapi.target_deploy('beta','deploy.'+pro)
                time.sleep(8)
                #db = db_operate()
                # sql = 'select returns from salt_returns where jid=%s'
                #ret=db.select_table(settings.RETURNS_MYSQL,sql,str(jid))    #通过jid获取执行结果
    return render(request,'deploy/code_distribution.html')


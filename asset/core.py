#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
from asset import models
from django.utils import timezone
class Asset(object):
    def __init__(self,request):
        self.request = request
        self.mandatory_fields = ['sn','asset_id','asset_type'] # 必需字段
        self.response = {
            'error':[],
            'info':[],
            'warning':[]
        }

    def response_msg(self,msg_type,key,msg):
        if msg_type in self.response:
            self.response[msg_type].append({key:msg})
        else:
            raise ValueError

    def get_asset_id_by_sn(self):
        data = self.request.POST.get('asset_data')
        response={}
        if data:
            try:
                data = json.loads(data)
                if self.mandatory_check(data,True): # 资产已在数据库，返回资产id
                    response = {'asset_id':self.asset_obj.id} # 获取到id
                else: # 新资产，需要批准
                    if hasattr(self,'waiting_approval'):
                        self.clean_data = data
                        self.save_new_asset_to_approval_zone()

            except Exception as e:
                print(e)
        else:
            self.response_msg('error','AssetDataInvalid','无效的资产数据')
        return response

    def save_new_asset_to_approval_zone(self):
        '''保存数据到批准区等待批准'''
        asset_sn = self.clean_data.get('sn')
        ram_size_to = self.clean_data.get('ram')
        ram_sum = 0
        for i in ram_size_to:
            ram = int(i['capacity'])
            ram_sum +=ram
        models.NewAssetApprovalZone.objects.get_or_create( sn=asset_sn,
                                                           data=json.dumps(self.clean_data),
                                                           manufactory=self.clean_data.get('manufactory'),
                                                           model=self.clean_data.get('model'),
                                                           asset_type=self.clean_data.get('asset_type'),
                                                           ram_size=ram_sum,
                                                           cpu_model=self.clean_data.get('cpu_model'),
                                                           cpu_count=self.clean_data.get('cpu_count'),
                                                           cpu_core_count=self.clean_data.get('cpu_core_count'),
                                                           os_distribution=self.clean_data.get('os_distribution'),
                                                           os_release=self.clean_data.get('os_release'),
                                                           os_type=self.clean_data.get('os_type'),
                                                                                           )
        return True

    def data_is_valid(self):
        data = self.request.POST.get("asset_data")
        if data:
            data = json.loads(data)
            if self.mandatory_check(data):
                self.clean_data = data
                return True
            else:
                return False
        else:
            print("没有资产数据")

    def mandatory_check(self,data,check_id=False):
        '''根据条件取出 asset_obj 对象'''
        for field in self.mandatory_fields:
            if field not in data:
                self.response_msg('error','MandatoryCheckFailed', "缺少必须的字段%s"%field)
                return False
        try:
            if check_id:
                self.asset_obj = models.Asset.objects.get(sn=data['sn'])
            else:
                self.asset_obj = models.Asset.objects.get(id=int(data['asset_id']),sn=data['sn'])
            return True
        except Exception as e:
            print(e)
            self.response_msg('error','AssetDataInvalid','数据库找不到资产对应的数据 id [%s] , SN [%s] ')
            self.waiting_approval = True#等待批准
            return False

    def data_into(self):
        if hasattr(self.asset_obj, self.clean_data['asset_type']):
            self.update_asset()
            print("update_asset")
        else:
            print("create_asset")
            self.create_asset()

    def data_is_valid_without_id(self):
        '''批准新资产时通过这里'''
        data = self.request.POST.get("asset_data")
        if data:
            try:
                data = json.loads(data)
                asset_obj = models.Asset.objects.get_or_create(sn=data.get('sn'),name=data.get('sn'))
                data['asset_id'] = asset_obj[0].id
                self.mandatory_check(data)
                self.clean_data = data
                if not self.response['error']:
                    return True
            except ValueError as e:
                self.response_msg('error','AssetDataInvalid', str(e))
        else:
            self.response_msg('error','AssetDataInvalid', "无效资产数据")

    def create_asset(self):
        func = getattr(self,'_create_%s' % self.clean_data['asset_type'])
        create_obj =func()

    def update_asset(self):
        func = getattr(self,'_update_%s' % self.clean_data['asset_type'])
        create_obj =func()
    #字段类型验证
    def  _type_validation(self,data_set,field_key,data_type):
        field_val = data_set.get(field_key)
        if field_val:
            try:
                data_set[field_key] = data_type(field_val)
            except Exception as e:
                self.response_msg('error','InvalidField', "[%s] 是无效数据类型, 正确的数据类型应该是 [%s] " % (field_key,data_type) )
        else:
            self.response_msg('error','LackOfField', "在 [%s] 中不存在 [%s]" % (data_set,field_key) )

    def _create_server(self):
        self.__create_server_into()
        self.__create_manufactory()
        self.__create_cpu()
        self.__create_disk()
        self.__create_nic()
        self.__create_ram()
    def __create_server_into(self):
        try:
            self._type_validation(self.clean_data,'model',str)
            if not len(self.response['error']):
                data_set = {
                            'asset_id' : self.asset_obj.id,
                            'raid_type': self.clean_data.get('raid_type'),
                            'model':self.clean_data.get('model'),
                            'os_type':self.clean_data.get('os_type'),
                            'os_distribution':self.clean_data.get('os_distribution'),
                            'os_release':self.clean_data.get('os_release'),
                        }
                obj = models.Server(**data_set)
                obj.save()
                return obj
        except Exception as e:
            self.response_msg('error','CreationException','Object [server] %s' % str(e) )
    def __create_manufactory(self):
        self._type_validation(self.clean_data,'manufactory',str)
        manufactory = self.clean_data.get('manufactory')
        try:
            if not len(self.response['error']):
                obj_mun = models.Manufactory.objects.filter(manufactory=manufactory)
                if obj_mun:#如果该厂商存在
                    obj = obj_mun[0]
                else:
                    obj = models.Manufactory(manufactory=manufactory)
                    obj.save()
                self.asset_obj.manufactory = obj
                self.asset_obj.save()
        except Exception as e:
            print(e)
            self.response_msg('error','CreationException','Object [manufactory] %s' % str(e) )
    def __create_cpu(self):
        try:
            self._type_validation(self.clean_data,'model',str)
            self._type_validation(self.clean_data,'cpu_count',int)
            self._type_validation(self.clean_data,'cpu_core_count',int)
            if not len(self.response['error']):
                data_set = {
                            'asset_id' : self.asset_obj.id,
                            'cpu_model': self.clean_data.get('cpu_model'),
                            'cpu_count':self.clean_data.get('cpu_count'),
                            'cpu_core_count':self.clean_data.get('cpu_core_count'),
                        }

                obj = models.CPU(**data_set)
                obj.save()
        except Exception as e:
            print(e)
            self.response_msg('error','CreationException','Object [cpu] %s' % str(e) )
    def __create_disk(self):
        disk_info = self.clean_data.get('physical_disk_driver')
        if disk_info:
            for disk_item in disk_info:
                try:
                    #self._type_validation(disk_item,'slot',str)
                    self._type_validation(disk_item,'capacity',float)
                    self._type_validation(disk_item,'iface_type',str)
                    self._type_validation(disk_item,'model',str)
                    if not len(self.response['error']): #no processing when there's no error happend
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'sn': disk_item.get('sn'),
                            'slot':disk_item.get('slot'),
                            'capacity':disk_item.get('capacity'),
                            'model':disk_item.get('model'),
                            'iface_type':disk_item.get('iface_type'),
                            'manufactory':disk_item.get('manufactory'),
                        }

                        obj = models.Disk(**data_set)
                        obj.save()
                except Exception as e:
                    print(e)
                    self.response_msg('error','CreationException','Object [disk] %s' % str(e) )
        else:
            self.response_msg('error','LackData','提交的内容没有 DISK 信息' )
    def __create_nic(self):
        nic_info = self.clean_data.get('nic')
        if nic_info:
            for nic_item in nic_info:
                try:
                    self._type_validation(nic_item,'macaddress',str)
                    if not len(self.response['error']): #no processing when there's no error happend
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'name': nic_item.get('name'),
                            'sn': nic_item.get('sn'),
                            'macaddress':nic_item.get('macaddress'),
                            'ipaddress':nic_item.get('ipaddress'),
                            'bonding':nic_item.get('bonding'),
                            'model':nic_item.get('model'),
                            'netmask':nic_item.get('netmask'),
                        }

                        obj = models.NIC(**data_set)
                        obj.save()
                except Exception as e:
                    print(e)
                    self.response_msg('error','CreationException','Object [nic] %s' % str(e) )
        else:
            self.response_msg('error','LackOfData','提交的内容没有 NIC 信息')
    def __create_ram(self):
        ram_info = self.clean_data.get('ram')
        if ram_info:
            for ram_item in ram_info:
                try:
                    self._type_validation(ram_item,'capacity',int)
                    if not len(self.response['error']): #no processing when there's no error happend
                        data_set = {
                            'asset_id' : self.asset_obj.id,
                            'slot': ram_item.get("slot"),
                            'sn': ram_item.get('sn'),
                            'capacity':ram_item.get('capacity'),
                            'manufactory':ram_item.get('manufactory'),
                            'model':ram_item.get('model'),
                        }

                        obj = models.RAM(**data_set)
                        obj.save()
                except Exception as e:
                    print(e)
                    self.response_msg('error','CreationException','Object [ram] %s' % str(e) )
        else:
            self.response_msg('error','LackOfData','提交的内容没有 RAM 信息' )

    def _update_server(self):
        #nic
        self.__update_asset(self.clean_data['nic'],
                            rev='nic_set',
                            contrast_fields = ['name','sn','model','macaddress','ipaddress','netmask','bonding'],
                            identify_field = 'macaddress'
                            )
        #disk
        self.__update_asset(self.clean_data['physical_disk_driver'],
                             rev='disk_set',
                             contrast_fields = ['slot','sn','model','manufactory','capacity','iface_type'],
                             identify_field = 'slot'
                                            )
        #ram
        self.__update_asset(data_source=self.clean_data['ram'],
                            rev='ram_set',
                            contrast_fields = ['slot','sn','model','capacity'],
                            identify_field = 'slot'
                                            )
        #cpu
        self.__update_cpu()
        #manufactory
        self.__update_manufactory()
        #server
        self.__update_server()

    def __update_asset(self,data_source,rev,contrast_fields,identify_field):

        try:
            print(data_source)
            set_obj = getattr(self.asset_obj,rev)#根据asset_obj反取关联的相应对象
            set_obj_result = set_obj.select_related()
            print(set_obj_result)
            for obj in set_obj_result:
                print(obj)
                db_field_data = getattr(obj,identify_field)#取出数据库该字段的值
                for data_source_item in data_source:
                    print(data_source_item)
                    dic_field_data = data_source_item[identify_field]#取出传入字典内该字段的值
                    if dic_field_data:
                        print(db_field_data,dic_field_data)
                        if db_field_data == dic_field_data:#如果相等，则进行对比
                            self.__compare_field(db_obj=obj,contrast_fields=contrast_fields,dic_obj=data_source_item)
                            break
                    else:
                        print("传入的数据没有该字段")
            #比较数据库的所有组件，查看是否有新增或删除

            model_obj_name=set_obj.model._meta.object_name  #取到表名，用于后面添加
            self.__compare_field_add_or_delete(model_obj_name,set_obj_result,data_source,identify_field)

        except Exception as e:
            print(e)

    def __update_cpu(self):
        update_fields = ['cpu_model','cpu_count','cpu_core_count']
        if hasattr(self.asset_obj,'cpu'):
            self.__compare_field(self.asset_obj.cpu,update_fields,self.clean_data)
        else:
            self.__create_cpu()

    def __update_manufactory(self):
        self.__create_manufactory()

    def __update_server(self):
        update_fields = ['model','os_type','os_distribution','os_release']
        if hasattr(self.asset_obj,'server'):
            self.__compare_field(self.asset_obj.server,update_fields ,self.clean_data)
        else:
            self.__create_server_into()

    def __compare_field(self,db_obj,contrast_fields,dic_obj):
        for field in contrast_fields:#循环要对比的字段列表
            db_field = getattr(db_obj,field)
            dic_field = dic_obj.get(field)
            print(field,db_field,dic_field)
            if dic_field:
                if type(db_field) is unicode:dic_field = unicode(dic_field).strip() #in py2.7
                if type(db_field) in (int,long):dic_field = int(dic_field) #in py2.7
                #if type(db_field) in (int,):dic_field = int(dic_field)
                elif type(db_field) is float:dic_field = float(dic_field)

                if db_field == dic_field:
                    pass
                else:
                    db_field_obj = db_obj._meta.get_field(field) #取出该字段的对象
                    db_field_obj.save_form_data(db_obj, dic_field) #把字段内容改为字典传入的内容
                    db_obj.update_date = timezone.now()
                    db_obj.save()

                    #记录日志
                    log_msg = "Asset [%s] ,component [%s] ,field [%s] has changed from [%s] to [%s]"%(self.asset_obj,db_obj,field,db_field,dic_field)
                    self.log_handler(self.asset_obj,'FieldChanged',self.request.user,log_msg,db_obj)

            else:
                print("没有该字段")

    def __compare_field_add_or_delete(self,model_obj_name,set_obj_result,data_source,identify_field):
        data_source_key_list = []
        set_obj_result_list = []
        if type(data_source) is list:
            for data in data_source:
                data_source_key_list.append(data[identify_field])
        dic_obj_list = set(data_source_key_list)

        for db_obj in set_obj_result:
            set_obj_result_list.append(getattr(db_obj,identify_field))
        db_obj_list = set(set_obj_result_list)

        data_only_in_db = db_obj_list - dic_obj_list    #delete_list 有值，到数据库删除多余数据
        data_only_in_dic = dic_obj_list - db_obj_list   #add_list 有值，到数据库增加数据
        #删除多余数据
        self.__delete_obj(set_obj_result,data_only_in_db,identify_field)

        #增加数据
        if data_only_in_dic:
            self.__add_obj(model_obj_name,data_source,data_only_in_dic,identify_field)

    def __add_obj(self,model_obj_name,data_source,data_only_in_dic,identify_field):
        model_obj = getattr(models,model_obj_name)#相当于models.表名
        create_list = []

        if type(data_source) is list:
            for data in data_source:
                if data[identify_field] in data_only_in_dic:
                    create_list.append(data)
        try:
            for memo in create_list:
                data_set = {}
                for field in model_obj.auto_create_fields:
                    data_set[field] = memo.get(field)
                data_set['asset_id'] = self.asset_obj.id
                obj = model_obj(**data_set)
                obj.save()
                print("add %s"%data_set)
                log_msg = "Asset[%s],component[%s] add [%s]" %(self.asset_obj,model_obj_name,data_set)
                self.log_handler(self.asset_obj,'NewComponentAdded',self.request.user,log_msg,model_obj_name)

        except Exception as e:
            print(e)

    def __delete_obj(self,set_obj_result,data_only_in_db,identify_field):
        delete_obj_list = []
        print(set_obj_result)
        for obj in set_obj_result:
            val = getattr(obj,identify_field)
            print(val)
            if val in data_only_in_db:
                delete_obj_list.append(obj)

        for i in delete_obj_list:
            log_msg = "Asset[%s], component[%s],已被删除或替换，将从数据库删除" %(self.asset_obj,i)
            self.response_msg('info','HardwareChanges',log_msg)
            self.log_handler(self.asset_obj,'HardwareChanges',self.request.user,log_msg,i)
            i.delete()

    # 记录日志
    def log_handler(self,asset_obj,event_name,user,log_msg,component=None):
        log_event={
            1 : ['FieldChanged','HardwareChanges'],
            2 : ['NewComponentAdded'],
        }
        if not user.id:
            user = models.User.objects.filter(is_admin=True).last()

        event_type= None
        for k,v in log_event.items():
            if event_name in v:
                event_type = k
                break
        log_obj = models.EventLog(
            name = event_name,
            event_type = event_type,
            asset_id = asset_obj.id,
            component = component,
            detail = log_msg,
            user_id = user.id
        )
        log_obj.save()





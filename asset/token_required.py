#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time,hashlib,json
from asset import models
from django.shortcuts import render,HttpResponse
from lyanadmin import settings
from django.core.exceptions import ObjectDoesNotExist

def gen_token(username,timestamp,token):
    token_format = "%s\n%s\n%s" %(username,timestamp,token)
    obj = hashlib.md5()
    obj.update(token_format)
    return obj.hexdigest()[10:17]


def token_required(func):
    def wrapper(*args,**kwargs):
        response = {"errors":[]}
        get_args = args[0].GET
        username = get_args.get("user")
        token_md5_from_client = get_args.get("token")
        timestamp = get_args.get("timestamp")

        if not username or not timestamp or not token_md5_from_client:
            response['errors'].append({"auth_failed":"This api requires token authentication!"})
            return HttpResponse(json.dumps(response))
        try:
            if abs(time.time() - int(timestamp)) > settings.TOKEN_TIMEOUT:#验证时间有没有超过2分钟
                response['errors'].append({"auth_failed":"The token is expired!"})
            else:
                '''如果没超过两分钟，检查redis里有没有这个加密token'''
                red_result = __redies_token(username,token_md5_from_client)
                if red_result:  #等于True说明是第一次请求，进入下一步验证
                    user_obj = models.MyUser.objects.get(email=username)
                    token_md5_from_server = gen_token(username,timestamp,user_obj.token)
                    if token_md5_from_client != token_md5_from_server:
                        response['errors'].append({"auth_failed":"Invalid username or token_id"})
                    else:

                        print("通过验证")
                else:
                    response['errors'].append({"auth_failed":"The token is expired!"})

                print("\033[41;1m;%s ---client:%s\033[0m" %(time.time(),timestamp), time.time() - int(timestamp))
        except ObjectDoesNotExist as e:
            response['errors'].append({"auth_failed":"Invalid username or token_id"})
        if response['errors']:
            return HttpResponse(json.dumps(response))
        else:
            return  func(*args,**kwargs)
    return wrapper

def __redies_token(username,token_md5_from_client):
    import redis
    r = redis.Redis(host='192.168.0.109', port=6379)
    val =  r.get(username)
    if val == token_md5_from_client:
        print("是以请求过的token")
        return False
    else:#不存在，则以用户名为key，加密的token为value存入缓存，存在时间2分钟
        r.set(username, token_md5_from_client,ex=120)
        return True



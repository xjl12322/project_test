#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/3/20 21:06"

import redis
zlcache = redis.Redis(host='127.0.0.1',port=6379,password=None,decode_responses=True)

def set(key,value,timeout=60):
    return zlcache.set(key,value,timeout)

def get(key):
    return zlcache.get(key)

def delete(key):
    return zlcache.delete(key)
# pool = redis.ConnectionPool(host='127.0.0.1',password='helloworld')   #实现一个连接池
#
# r = redis.Redis(connection_pool=pool)
# r.set('foo','bar')
# print(r.get('foo').decode('utf8'))







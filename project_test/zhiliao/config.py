#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/2/28 23:31"

import os

# SECRET_KEY = os.urandom(24)
SECRET_KEY = 'ddfdffd'


DEBUG = True

DB_USERNAME = 'root'
DB_PASSWORD = 'mysql'
DB_HOST = '127.0.0.1'
DB_PORT = '3306'
DB_NAME = 'test'
# PERMANENT_SESSION_LIFETIME =
from datetime import timedelta


DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=3)

CMS_USER_ID = 'user_id'
FRONT_USER_ID = "fort_id"
# MAIL_USE_TLS：端口号587
# MAIL_USE_SSL：端口号465
# QQ邮箱不支持非加密方式发送邮件
# 发送者邮箱的服务器地址
MAIL_SERVER = "smtp.163.com"
MAIL_PORT = '465'
# MAIL_USE_TLS = True
MAIL_USE_SSL = True
MAIL_USERNAME = "xjl12322@163.com"
MAIL_PASSWORD = "xjl12322"
MAIL_DEFAULT_SENDER = "xjl12322@163.com"

#分页配置
PER_PAGE = 10



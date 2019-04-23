#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/3/15 21:07"
from flask  import session,redirect,url_for,g
from functools import wraps
from config import CMS_USER_ID


def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if CMS_USER_ID in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner

def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args,**kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outter




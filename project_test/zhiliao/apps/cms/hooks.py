#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/3/16 15:59"

from config import *
from flask import session,g
from .models import CMSUser
from .models import CMSPersmission
from .views import bp
@bp.before_request
def before_request():
    if CMS_USER_ID in session:
        user_id = session.get(CMS_USER_ID)
        user = CMSUser.query.get(user_id)
        if user:
            g.cms_user = user


@bp.context_processor
def cms_context_processor():
    return ({"CMSPermission":CMSPersmission})


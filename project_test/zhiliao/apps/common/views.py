#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/2/28 23:15"


from flask import Blueprint,make_response,session,request
from io import BytesIO
from utils.captcha import Captcha
from utils.yuntongxun.sms import CCP
from utils import restful
from .froms import SMSCaptchaForm
from .zlcache import zlcache
bp = Blueprint("common",__name__,url_prefix='/common')


@bp.route("/")
def index():
    return "cms index"

@bp.route("/captcha")
def graph_captcha():
    '''
    图片验证码发送
    :return:  二进制流对象
    '''
    text,image = Captcha.gene_graph_captcha()
    zlcache.set(text.lower(),text.lower())
    zlcache.expire(text.lower(),60*5)
    out = BytesIO()
    image.save(out,"png")
    buf_str = out.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/png'
    # session['img'] = text.upper()
    return response

# @bp.route("/sms_captcha")
# def cms_captcha():
#     '''
#     短信验证码发送
#     :return:  成功和失败
#     '''
#     telephone = request.args.get("telephone")
#     if not telephone:
#         return restful.params_error("请输入手机号")
#     ccp = CCP()
#     # 注意： 测试的短信模板编号为1
#     captcha = Captcha.gene_text(number=4)
#     status = ccp.send_template_sms(str(telephone).strip(), [captcha,5], 1)
#     if status == 0:
#         return restful.success()
#     else:
#         return restful.params_error(message="短信验证发送失败")

@bp.route("/sms_captcha/",methods=["POST"])
def cms_captcha():
    '''
    短信验证加密发送
    :return:  成功和失败
    '''
    form = SMSCaptchaForm(request.form)
    if form.validate():
        telephone = form.telephone.data

        ccp = CCP()
        captcha = Captcha.gene_text(number=4).lower()
        status = ccp.send_template_sms(str(telephone).strip(), [captcha,5], 1)
        if status == 0:

            zlcache.set(str(telephone),captcha)
            zlcache.expire(str(telephone), 60*5)
            return restful.success()

        else:
            return restful.params_error(message="短信验证发送失败")
    else:
        return restful.params_error(message="参数错误{}".format(form.errors))

@bp.route('/uptoken/')
def uptoken():
    access_key = 'M4zCEW4f9XPanbMN-Lb9O0S8j893f0e1ezAohFVL'
    secret_key = '7BKV7HeEKM3NDJk8_l_C89JI3SMmeUlAIatzl9d4'
    q = qiniu.Auth(access_key,secret_key)

    bucket = 'hyvideo'
    token = q.upload_token(bucket)
    return jsonify({'uptoken':token})

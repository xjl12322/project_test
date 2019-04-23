#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/2/28 23:15"
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify
from .froms import *
from .models import CMSUser,CMSPersmission
from .decorators import login_required,permission_required
from config import CMS_USER_ID
from exts import db,mail
from utils import restful
from flask_mail import Message
import string,random
from ..common.zlcache import zlcache
from apps.models import *
bp = Blueprint("cms",__name__,url_prefix='/cms')
@bp.route("/")
@login_required
def index():
    '''
    cms首页
    :return:
    '''
    return render_template('cms/cms_index.html')

@bp.route("/loginout")
def loginout():
    '''
    cms注销
    :return:
    '''
    # session.clear() 或
    del session[CMS_USER_ID]
    return redirect(url_for("cms.login"))
@bp.route("/profile")
@login_required
def profile():
    return render_template('cms/cms_profile.html')

# @bp.route("/email")
# @login_required
# def send_email():


@bp.route("/email_captcha/")
@login_required
def send_email():
    email =  request.args.get("email")
    if not email:
        return restful.params_error("请传递邮箱参数")
    source = list(string.ascii_letters)
    source.extend(map(lambda  x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,6))
    message = Message("知了课堂", recipients=[email], body="验证码是{}".format(captcha))
    try:
        mail.send(message=message)
    except Exception as e:
        return restful.server_error(message="邮箱服务器发送错误")
    zlcache.set(email,captcha)
    return restful.success()


@bp.route("/posts/")
@login_required
@permission_required(CMSPersmission.POSTER)
def posts():
    context = {"posts": PostModel.query.all()}
    return render_template("cms/cms_posts.html",**context)

@bp.route("/hpost/",methods = ["POST"])
@login_required
@permission_required(CMSPersmission.POSTER)
def hpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error("请传入帖子")
    post =PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子")
    highlight = HighlightPostModel()
    highlight.post = post
    db.session.add(highlight)
    db.session.commit()
    return restful.success()

@bp.route('/uhpost/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.POSTER)
def uhpost():
    post_id = request.form.get("post_id")
    if not post_id:
        return restful.params_error('请传入帖子id！')
    post = PostModel.query.get(post_id)
    if not post:
        return restful.params_error("没有这篇帖子！")

    highlight = HighlightPostModel.query.filter_by(post_id=post_id).first()
    db.session.delete(highlight)
    db.session.commit()
    return restful.success()


@bp.route("/comments/")
@login_required
@permission_required(CMSPersmission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")


@bp.route("/aboard/",methods=["POST"])
@login_required
@permission_required(CMSPersmission.BOARDER)
def aboard():
    '''
    cms板块添加
    :return:
    '''
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        board = BoardModel(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/uboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def uboard():
    '''
    板块更新
    :return:
    '''
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = BoardModel.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/',methods=['POST'])
@login_required
@permission_required(CMSPersmission.BOARDER)
def dboard():
    '''
    cms板块删除
    :return:
    '''
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error('请传入板块id！')
    board = BoardModel.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')
    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route("/boards/")
@login_required
@permission_required(CMSPersmission.BOARDER)
def boards():
    '''
    板块页
    :return:
    '''
    board_models = BoardModel.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html',**context)



@bp.route("/fusers/")
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")
@bp.route("cusers")
@login_required
@permission_required(CMSPersmission.FRONTUSER)
def cusers():
    return render_template("cms/cms_cusers.html")

@bp.route("croles")
@login_required
@permission_required(CMSPersmission.CMSUSER)
def croles():
    return render_template("cms/cms_croles.html")


@bp.route('/banners')
@login_required
def banners():
    '''
    cms后台轮播图列表获取
    :return:
    '''
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).all()
    return render_template("cms/cms_banners.html",banners = banners)
@bp.route('/ubanner/',methods=['POST'])
@login_required
def ubanner():
    '''
    cms后台轮播图列表更新
    :return:
    '''
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())

@bp.route('/dbanner/',methods=["POST"])
@login_required
def dbanners():
    '''
    cms后台轮播图删除
    :return:
    '''
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = BannerModel.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()
@bp.route('/abanner',methods=["POST"])
@login_required
def abanners():
    '''
    cms后台轮播图添加
    :return:
    '''
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = BannerModel(name=name,image_url=image_url,link_url=link_url,priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())

class ResetPwdView(views.MethodView):
    '''
    cms密码重置
    :return:
    '''
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetpwd.html')
    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误！")
        else:
            return restful.params_error(form.get_error())

class LoginView(views.MethodView):
    '''
    cms登录模块
    '''
    def get(self,message = None):
        return render_template("cms/cms_login.html",message=message)
    def post(self,message = None):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = CMSUser.query.filter_by(email = email).first()

            if user and user.check_password(password):
                session[CMS_USER_ID] = user.id
                if remember:
                    #默认设置cookie31天
                    session.permanent = False
                return redirect(url_for("cms.index"))
            else:
                return self.get(message = "邮箱或密码错误")
        else:
            '''多个错误{'password': ['请输入正确格式的密码'],'email‘:['邮箱错误]'}'''
            message = form.get_error()
            return self.get(message = message)

class ResetEmailView(views.MethodView):
    '''
    cms邮箱重置
    :return:
    '''
    decorators = [login_required]
    def get(self):
        return render_template('cms/cms_resetemail.html')
    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))



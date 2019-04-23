#! /usr/bin/env python3
# -*- coding:utf-8 -*-
from apps.models import *

__author__ = "X"
__date__ = "2019/2/28 23:15"
from flask import Blueprint,views,render_template,request,session,redirect,url_for,g,jsonify,make_response,abort
from .froms import *
from .models import FrontUser
from .decorators import login_required
import config
from exts import db
from utils import restful,safeutils
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy import func
bp = Blueprint("front",__name__)


@bp.route("/")
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    sort = request.args.get("st",type=int,default=1)
    banners = BannerModel.query.order_by(BannerModel.priority.desc()).limit(4)
    boards = BoardModel.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    pasts = None
    total = 0

    query_obj = None
    if sort == 1:
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(PostModel).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),PostModel.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(PostModel).outerjoin(CommentModel).group_by(PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(PostModel.board_id==board_id)
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        posts = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'posts': posts,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html',**context)


@bp.route('/p/<post_id>/',methods=['GET','POST'])
def post_detail(post_id):
    '''
    帖子详情
    :param post_id:
    :return:
    '''
    post = PostModel.query.get(post_id)
    if not post:
        abort(404)
    return render_template("front/front_pdetail.html", post = post)


@bp.route('/acomment/',methods=['GET','POST'])
@login_required
def acomment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        post = PostModel.query.get(post_id)
        if post:
            comment = CommentModel(content=content)
            comment.post = post
            comment.author = g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这篇帖子！')
    else:
        return restful.params_error(form.get_error())


@bp.route('/apost/',methods=['GET','POST'])
@login_required
def apost():
    '''
    添加帖子
    :return:
    '''
    if request.method == 'GET':
        boards = BoardModel.query.all()
        return render_template("front/front_apost.html",boards = boards)
    else:
        form = AddPostForm(request.form)

        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = BoardModel.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            post = PostModel(title=title,content=content)
            post.board = board
            post.author = g.front_user
            db.session.add(post)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())






class SigninView(views.MethodView):
    '''
    账号登录
    :return:
    '''
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and return_to != url_for("front.signup") and safeutils.is_safe_url(return_to):
            return render_template('front/front_signin.html',return_to=return_to)
        else:
            return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remeber.data
            user = FrontUser.query.filter_by(telephone=telephone).first()
            if user and user.check_password(password):
                session[config.FRONT_USER_ID] = user.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())


class SignupView(views.MethodView):
    '''
    账号注册
    :return:
    '''
    def get(self):
        return_to = request.referrer
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            return render_template("front/front_signup.html",return_to=return_to)
        else:
            return render_template('front/front_signup.html')

    def post(self):
        form = SignupForm(request.form)
        # assert False
        if form.validate():
            if form.validate():
                telephone = form.telephone.data
                username = form.username.data
                password = form.password1.data
                user = FrontUser(telephone=telephone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error(message=form.get_error())
        else:
            return restful.params_error(message="参数验证异常")



bp.add_url_rule("/signup/",view_func= SignupView.as_view("signup"))
bp.add_url_rule("/signin/",view_func= SigninView.as_view("signin"))


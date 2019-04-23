#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/3/17 15:37"
from wtforms import StringField,IntegerField,Form
from wtforms.validators import Email,InputRequired,Length,EqualTo
# from ..forms import BaseForm
class BaseForm(Form):

    def get_error(self):
        message = self.errors.popitem()[1][0]
        return message


    def validate(self):
        return super(BaseForm,self).validate()
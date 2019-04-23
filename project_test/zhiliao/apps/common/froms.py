#! /usr/bin/env python3
# -*- coding:utf-8 -*-
__author__ = "X"
__date__ = "2019/2/28 23:16"
from apps.forms import BaseForm
from wtforms import StringField
from wtforms.validators import regexp,InputRequired
import hashlib
class SMSCaptchaForm(BaseForm):
    salt = 'q3423805gdflvbdfvhsdoa`#$%'
    telephone = StringField(validators=[regexp(r'1[345789]\d{9}')])
    timestamp = StringField(validators=[regexp(r'\d{12}')])
    sign = StringField(validators=[InputRequired()])

    def validate(self):
        result = super().validate()
        if not result:
           return False

        telephone = self.telephone.data
        timestamp = self.timestamp.data
        sign = self.sign.data
        sign2 = hashlib.md5((timestamp + telephone + self.salt).encode('utf-8')).hexdigest()
        if sign == sign2:
            return True
        else:
            return False






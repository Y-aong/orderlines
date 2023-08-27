# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : token_view.py
# Time       ：2023/7/9 16:49
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    token 视图
    token view
"""
from flask import request
from flask_restful import Resource

from apis.system_oauth.models import SystemUser
from conf.config import FlaskConfig
from public.api_handle_exception import handle_api_error
from public.base_response import generate_response
from public.api_utils.jwt_utils import generate_token


class TokenView(Resource):
    url = '/token'

    def __init__(self):
        self.form_data = request.json
        self.login_types = {
            'username': self.form_data.get('username'),
            'email': self.form_data.get('email'),
            'phone': self.form_data.get('phone'),
        }
        self.login_type = self.form_data.get('login_type')

    def generate_payload(self):
        login_value = self.form_data.get(self.login_type)
        password = self.form_data.get('password')
        SystemUser.check_password(password, self.login_type, login_value)
        return {
            'login_type': self.login_type,
            'login_value': login_value,
            'password': password
        }

    @handle_api_error
    def post(self):
        pay_load = self.generate_payload()
        token = generate_token(pay_load, expiry=FlaskConfig.EXPIRY)
        return generate_response(token)

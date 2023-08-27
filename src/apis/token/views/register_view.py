# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : register_view.py
# Time       ：2023/8/26 22:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    用户注册
"""
from flask import request
from flask_restful import Resource

from apis.system_oauth.models import SystemUser
from public.api_handle_exception import handle_api_error
from public.base_model import db
from public.base_response import generate_response


class RegisterView(Resource):
    url = '/register'

    def __init__(self):
        self.username = request.json.get('username')
        self.password = request.json.get('password')
        self.email = request.json.get('email')
        self.phone = request.json.get('phone')

    @handle_api_error
    def post(self):
        if not self.username or self.password:
            raise ValueError('username or password can not been null')
        user_info = {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone': self.phone,
        }

        with db.auto_commit():
            obj = SystemUser(**user_info)
            db.session.add(obj)

        return generate_response(message=f'user {self.username} register success!')
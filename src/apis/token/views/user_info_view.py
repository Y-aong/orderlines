# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_info_view.py
# Time       ：2023/8/26 22:56
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    根据token获取用户
"""
from flask import request
from flask_restful import Resource

from public.api_handle_exception import handle_api_error
from public.api_utils.jwt_utils import verify_token
from public.base_response import generate_response


class UserTokenView(Resource):
    url = '/user_info'

    def __init__(self):
        self.token = request.args.get('token')

    @handle_api_error
    def get(self):
        payload = verify_token(self.token)
        return generate_response(payload)

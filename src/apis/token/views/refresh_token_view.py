# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : refresh_token_view.py
# Time       ：2023/8/26 23:00
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    刷新token
"""
from flask import request
from flask_restful import Resource

from public.api_handle_exception import handle_api_error
from public.api_utils.jwt_utils import refresh_token
from public.base_response import generate_response


class RefreshTokenView(Resource):
    url = '/refresh_token'

    def __init__(self):
        self.token = request.json.get('token')

    @handle_api_error
    def post(self):
        token = refresh_token(self.token)
        return generate_response(token)

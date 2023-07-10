# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : web_hook.py
# Time       ：2023/7/9 22:37
# Author     ：Y-aong
# version    ：python 3.7
# Description：web钩子函数
"""
from flask import request, Flask
from jwt import DecodeError

from public.api_exceptions.api_exceptions import JWTVerifyException
from public.base_response import generate_abort, generate_response
from public.api_utils.jwt_utils import verify_token
from public.logger import logger


class WebHook:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        self.black_list = ['/refresh_token']
        self.white_list = ['/token']

    def init_app(self, app: Flask):
        app.before_request(self.authentication)

    def check_black_list(self):
        if request.path in self.black_list:
            logger.info(f'已阻止黑名单{request.path}')
            return generate_abort(code=401, message='黑名单用户')

    def check_white_list(self):
        return True if request.path in self.white_list else False

    def authentication(self):
        """权限认证"""

        self.check_black_list()
        if not self.check_white_list():
            # 检查token
            authorization = request.headers.get('Authorization')
            if authorization and authorization.startswith('Bearer '):
                token = authorization.replace('Bearer ', '')
                try:
                    verify_token(token)
                except JWTVerifyException:
                    return generate_abort(400, message='token过期请重新登录')
                except DecodeError:
                    return generate_abort(400, message='token验证失败，请检查用户名密码')
            else:
                return generate_abort(401, message='认证失败，用户未认证')

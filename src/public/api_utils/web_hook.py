# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : web_hook.py
# Time       ：2023/7/9 22:37
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    web钩子函数
    web hook function
"""
from flask import request, Flask
from jwt import DecodeError

from public.api_exceptions.api_exceptions import JWTVerifyException
from public.api_utils.permission_utils import get_user_id_by_payload, get_user_role_permission, get_role_by_user

from public.base_response import generate_abort
from public.api_utils.jwt_utils import verify_token
from public.logger import logger


class WebHook:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
        self.black_list = []
        self.white_list = ['/refresh_token', '/token', '/register']

    def init_app(self, app: Flask):
        app.before_request(self.authentication)

    def check_black_list(self):
        if request.path in self.black_list:
            logger.info(f'Blocked blacklist {request.path}')
            return generate_abort(code=401, message='url in blacklist')

    def check_white_list(self):
        return True if request.path in self.white_list else False

    @staticmethod
    def check_role_permission(user_id):
        """检查用户角色权限, Check user role permissions"""
        permissions = get_user_role_permission(user_id)
        role = get_role_by_user(user_id)
        if role == 'admin':
            return True
        path = request.path
        method = request.method
        for permission in permissions:
            if permission.get('path') == path and permission.get('method') == method:
                return True
        return False

    @staticmethod
    def check_group_permission(user_id):
        """检查用户群组权限,Check user group permissions"""
        permissions = get_user_role_permission(user_id)
        path = request.path
        method = request.method
        for permission in permissions:
            if permission.get('path') == path and permission.get('method') == method:
                return True
        return False

    def authentication(self):
        """权限认证, Permission authentication"""
        self.check_black_list()
        if not self.check_white_list():
            authorization = request.headers.get('Authorization')
            if authorization and authorization.startswith('Bearer '):
                token = authorization.replace('Bearer ', '')
                try:
                    payload = verify_token(token)
                    user_id = get_user_id_by_payload(payload)
                    role_permission = self.check_role_permission(user_id)
                    group_permission = self.check_group_permission(user_id)
                    if not role_permission and not group_permission:
                        return generate_abort(401, data='Permission Denied')
                except JWTVerifyException:
                    return generate_abort(400, data='Please login again after the token expires.')
                except DecodeError:
                    return generate_abort(400, data='Please check the user name and password.')
            else:
                return generate_abort(401, data='Authentication failed because the user is not authenticated.')

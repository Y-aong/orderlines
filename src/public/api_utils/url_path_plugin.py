# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : url_path_plugin.py
# Time       ：2023/7/19 21:52
# Author     ：Y-aong
# version    ：python 3.7
# Description：获取全部的url路径
"""
from flask import Flask

from apis.system_oauth.models import SystemPermission
from public.base_model import get_session


class UrlPathPlugin:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
        self.names = {
            'GET': '增加',
            'POST': '创建',
            'PUT': '修改',
            'DELETE': '删除',
        }

    def init_app(self, app: Flask):
        self.get_url_path_method(app)

    def get_url_path_method(self, app: Flask):
        """获取所有的请求路径和请求方法"""
        rules = app.url_map.__dict__['_rules']
        for index in range(len(rules)):
            url_path = str(app.url_map.__dict__['_rules'][index])
            _methods = list(app.url_map.__dict__['_rules'][index].methods)
            methods = [item for item in _methods if item in self.methods]
            for method in methods:
                name = f'{url_path.replace("/", "")}_{method}'
                desc = f'{self.names.get(method)}_{url_path.replace("/", "")}'
                permission = {
                    'name': name,
                    'method': method,
                    'path': url_path,
                    'desc': desc,
                    'active': 1
                }
                session = get_session()
                permission_obj = session.query(SystemPermission).filter(
                    SystemPermission.path == url_path, SystemPermission.method == method).first()
                if not permission_obj:
                    obj = SystemPermission(**permission)
                    session.add(obj)
                    session.commit()

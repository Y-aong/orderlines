# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : default_config_plugin.py
# Time       ：2023/7/19 21:52
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    获取全部的url路径
    Gets all url paths
"""
from flask import Flask

from apis.system_oauth.models import SystemPermission
from public.base_model import get_session


class DefaultConfig:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

        self.methods = ['GET', 'POST', 'PUT', 'DELETE']
        self.names = {
            'GET': 'get',
            'POST': 'create',
            'PUT': 'update',
            'DELETE': 'delete',
        }

    def init_app(self, app: Flask):
        self.get_url_path_method(app)

    def get_url_path_method(self, app: Flask):
        """
        获取所有的请求路径和请求方法,
        Gets all request paths and request methods
        """
        rules = app.url_map.__dict__['_rules']
        for index in range(len(rules)):
            url_path = str(app.url_map.__dict__['_rules'][index])
            _methods = list(app.url_map.__dict__['_rules'][index].methods)
            methods = [item for item in _methods if item in self.methods]
            for method in methods:
                name = f'{url_path.replace("/", "")}_{self.names.get(method).lower()}'
                desc = f'{self.names.get(method).lower()}_{url_path.replace("/", "")}'
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

    def create_super_admin(self):
        """
        创建默认的超级管理员用户。
        Create a default super administrator
        """
        pass

    def create_default_config(self):
        """
        创建orderlines默认配置
        create orderlines default config
        @return:
        """

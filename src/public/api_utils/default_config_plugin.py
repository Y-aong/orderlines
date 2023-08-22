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

from apis.config.models import BaseConfig
from apis.system_oauth.models import SystemPermission, SystemUser, SystemRole, SystemUserRoleRelation
from public.base_model import get_session


class DefaultConfig:
    def __init__(self, app=None):
        self.session = get_session()
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
        self.create_default_config()

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

                permission_obj = self.session.query(SystemPermission).filter(
                    SystemPermission.path == url_path, SystemPermission.method == method).first()
                if not permission_obj:
                    obj = SystemPermission(**permission)
                    self.session.add(obj)
                    self.session.commit()

    def create_user(self, username='admin', password='admin', email='', phone='', admin=False):
        """
        创建默认的超级管理员用户。
        Create a default super administrator
        """
        user_info = {
            'username': username,
            'password': password,
            'email': email,
            'phone': phone,

        }
        obj = SystemUser(**user_info)
        self.session.add(obj)
        self.session.commit()
        user_id = obj.id
        # bind role
        if admin:
            admin_role = self.session.query(SystemRole).filter(SystemRole.role_name == 'admin').first()
            if not admin_role:
                obj = SystemRole({'role_name': 'admin', 'desc': 'super admin'})
                self.session.add(obj)
                self.session.commit()
                admin_role_id = obj.id
            else:
                admin_role_id = admin_role.id
            user_role_obj = SystemUserRoleRelation(**{'user_id': user_id, 'role_id': admin_role_id})
            self.session.add(user_role_obj)
            self.session.commit()

    def create_default_config(self):
        """
        创建orderlines默认配置
        create orderlines default config
        @return:
        """
        default_configs = [
            {
                'config_name': 'stop_all_schedule',
                'config_value': '1'
            }
        ]
        for item in default_configs:
            obj = BaseConfig(**item)
            self.session.add(obj)
            self.session.commit()

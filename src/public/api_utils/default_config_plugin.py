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
        from public.api_utils.jwt_utils import encrypt_password
        user_info = {
            'username': username,
            'password': encrypt_password(password),
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
                obj = SystemRole(**{'role_name': 'admin', 'desc': 'super admin'})
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
        from apis.config.models import BaseConfig
        default_configs = [
            {
                'config_name': 'stop_all_schedule',
                'config_value': '1',
                'desc': '定时任务总开关，1定时任务生效，0定时任务不生效。'
            },
            {
                'config_name': 'retry_time',
                'config_value': '3',
                'desc': '重试次数。默认为重试3次。',
            },
            {
                'config_name': 'sleep_time',
                'config_value': '1',
                'desc': '重试策略的休眠时间。默认为1秒。',
            },
            {
                'config_name': 'task_timeout',
                'config_value': '120',
                'desc': '默认任务的超时时间。默认120秒。',
            },
            {
                'config_name': 'process_timeout',
                'config_value': '120',
                'desc': '默认流程的超时时间。默认为120秒。',
            },
            {
                'config_name': 'notice_type',
                'config_value': 'FAILURE',
                'desc': '失败情况下进行回调。默认为失败，可选为失败、成功、重试、忽略、跳过。'
            },
            {
                'config_name': 'task_strategy',
                'config_value': 'RAISE',
                'desc': '任务异常处理策略。默认为报错，可选为报错，重试，忽略。'
            },
            {
                'config_name': 'callback_module',
                'config_value': 'Email',
                'desc': '任务异常回调方法。默认为邮件。'
            }

        ]
        for item in default_configs:
            obj = self.session.query(BaseConfig).filter(
                BaseConfig.config_name == item.get('config_name'),
                BaseConfig.active == 1
            ).first()
            if not obj:
                conf = BaseConfig(**item)
                self.session.add(conf)
                self.session.commit()

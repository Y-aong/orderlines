# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : task_node_view.py
# Time       ：2023/9/14 9:29
# Author     ：YangYong
# version    ：python 3.10
# Description：
    获取任务节点
    get task node
"""
from flask import request
from flask_restful import Resource

from apis.config.models import BaseConfig, PluginInfo
from apis.config.schema.base_config_schema import DefaultTaskConfigSchema
from apis.config.schema.plugin_info_schema import NodeParamSchema, NodeResultSchema, NodeConfigSchema
from orderlines.utils.orderlines_enum import TaskStatus
from public.api_handle_exception import handle_api_error
from public.base_model import db
from public.base_response import generate_response


class TaskNodeView(Resource):
    url = '/task_node'

    def __init__(self):
        self.form_data = request.args
        self.default_task_config = [
            'task_timeout',
            'task_strategy',
            'notice_type',
            'callback_module',
            'retry_time',
            'sleep_time',
        ]
        self.task_strategy = [
            {
                'value': 'RAISE',
                'label': '报错',
            },
            {
                'value': 'RETRY',
                'label': '重试',
            },
            {
                'value': 'SKIP',
                'label': '忽略',
            }
        ]
        self.notice_type = [
            {
                'value': TaskStatus.red.value,
                'label': '失败',
            },
            {
                'value': TaskStatus.green.value,
                'label': '成功',
            },
            {
                'value': TaskStatus.orange.value,
                'label': '重试',
            },
            {
                'value': TaskStatus.pink.value,
                'label': '忽略',
            }
        ]

    def get_default_task_config(self):
        objs = db.session.query(BaseConfig).filter(
            BaseConfig.config_name.in_(self.default_task_config)).all()

        data = DefaultTaskConfigSchema().dump(objs, many=True)
        default_task_config = list()
        for item in data:
            if item.get('config_name') == 'task_strategy':
                item['config_value'] = self.task_strategy
            elif item.get('config_name') == 'notice_type':
                item['config_value'] = self.notice_type
            default_task_config.append(item)
        return default_task_config

    def get_node_param_result(self):
        obj = db.session.query(PluginInfo).filter(
            PluginInfo.method_name == self.form_data.get('method_name'),
            PluginInfo.class_name == self.form_data.get('class_name'),
            PluginInfo.version == self.form_data.get('version')
        ).first()
        node_param = NodeParamSchema().dump(obj)
        node_result = NodeResultSchema().dump(obj)
        return node_param, node_result

    def get_node_config(self):
        obj = db.session.query(PluginInfo).filter(
            PluginInfo.method_name == self.form_data.get('method_name'),
            PluginInfo.class_name == self.form_data.get('class_name'),
            PluginInfo.version == self.form_data.get('version')
        ).first()
        return NodeConfigSchema().dump(obj)

    @handle_api_error
    def get(self):
        node_param, node_result = self.get_node_param_result()
        node_config = self.get_node_config()
        default_task_config = self.get_default_task_config()
        data = {
            'nodeConfig': node_config,
            'nodeParam': node_param,
            'nodeResult': node_result,
            'defaultTaskConfig': default_task_config
        }
        return generate_response(data, message='success')

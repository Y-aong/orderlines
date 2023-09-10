# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : default_task_config_view.py
# Time       ：2023/9/7 22:43
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    默认的任务配置参数
    default task config
"""
from flask_restful import Resource

from apis.config.models import BaseConfig
from apis.config.schema.base_config_schema import DefaultTaskConfigSchema
from orderlines.utils.orderlines_enum import TaskStatus
from public.base_model import db
from public.base_response import generate_response


class DefaultTaskConfigView(Resource):
    url = '/default_task_config'

    def __init__(self):
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

    def get(self):
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

        return generate_response(default_task_config)

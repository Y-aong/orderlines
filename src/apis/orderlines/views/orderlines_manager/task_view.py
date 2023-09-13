# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_view.py
# Time       ：2023/3/12 10:32
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    任务视图
    task view
"""
from flask import request

from apis.orderlines.models.task import Task
from apis.orderlines.schema.task_schema import TaskSchema
from public.base_model import db
from public.base_view import BaseView


class TaskView(BaseView):
    url = '/task'

    def __init__(self):
        super(TaskView, self).__init__()
        self.table_orm = Task
        self.table_schema = TaskSchema

    def handle_request_params(self):
        if request.method == 'PUT':
            obj = db.session.query(Task).filter(Task.id == self.table_id).first()
            info = TaskSchema().dump(obj)
            method_kwargs: dict = info.get('method_kwargs')
            result_config: dict = info.get('result_config')
            task_config: dict = info.get('task_config')
            _method_kwargs = self.form_data.get('method_kwargs')
            _result_config = self.form_data.get('result_config')
            _task_config = self.form_data.get('task_config')
            if method_kwargs and _method_kwargs and isinstance(_method_kwargs, dict):
                for key, val in _method_kwargs.items():
                    if key and val:
                        method_kwargs[key] = val
                self.form_data['method_kwargs'] = method_kwargs
            # 增加返回值
            if result_config and _result_config and isinstance(_result_config, dict):
                for key, val in _result_config.items():
                    if key and val:
                        result_config[key] = val
                self.form_data['result_config'] = result_config
            # 修改任务配置
            if task_config and _task_config and isinstance(_task_config, dict):
                for key, val in _task_config.items():
                    if key and val:
                        task_config[key] = val
                self.form_data['task_config'] = task_config

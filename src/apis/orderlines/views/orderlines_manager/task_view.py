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
from copy import deepcopy
from flask import request

from apis.orderlines.models.task import Task, TaskInstance
from apis.orderlines.schema.task_schema import TaskSchema
from public.base_model import db, get_session
from public.base_response import generate_response
from public.base_view import BaseView


class TaskView(BaseView):
    url = '/task'

    def __init__(self):
        super(TaskView, self).__init__()
        self.table_orm = Task
        self.table_schema = TaskSchema
        self.items = [
            'method_kwargs', 'result_config', 'task_config'
        ]

    def update_task_item(self, item_name: str):
        """修改巡视任务的item中的值"""
        obj = db.session.query(Task).filter(Task.id == self.table_id).first()
        info = TaskSchema().dump(obj)
        item: dict = deepcopy(info.get(item_name) or {})
        _item: dict = deepcopy(self.form_data.get(item_name))
        if item and _item and isinstance(_item, dict):
            for key, val in _item.items():
                if key and val:
                    item[key] = val
            self.form_data[item_name] = item

    def handle_request_params(self):
        if request.method == 'PUT':
            for key, val in self.form_data.items():
                if key in self.items:
                    self.update_task_item(key)

    def delete(self):
        session = get_session()
        # 删除任务实例
        session.query(TaskInstance).filter(TaskInstance.task_id == self.form_data.get('task_id')).delete()
        session.commit()
        session.flush()
        # 删除任务
        session.query(Task).filter(
            Task.task_id == self.form_data.get('task_id')).delete()
        session.commit()
        session.flush()
        return generate_response(message='删除节点成功')

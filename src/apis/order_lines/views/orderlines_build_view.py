# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_build_view.py
# Time       ：2023/3/12 13:22
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    创建流程视图
    build process view
"""

from flask import request

from flask_restful import Resource

from apis.order_lines.models import Task
from apis.order_lines.models.process import Process
from apis.order_lines.schema.process_schema import ProcessSchema
from apis.order_lines.schema.task_schema import TaskSchema
from public.base_model import db
from public.base_response import generate_response


class OrderLinesBuildView(Resource):
    url = '/orderlines/build'

    def __init__(self):
        self.form_data = request.json

    def post(self):
        process_info = self.form_data.get('process_info')
        node_info = self.form_data.get('process_node')
        process_id = process_info.get('process_id')
        # 生成process
        process = ProcessSchema().load(process_info)
        process_obj = db.session.query(Process).filter(Process.process_id == process_id).first()
        if process_obj:
            db.session.query(Process).filter(Process.process_id == process_id).update(process)
        else:
            process_obj = Process(**process)
            db.session.add(process_obj)
        db.session.commit()
        # generate task
        for node in node_info:
            node['process_id'] = process_id
            task_obj = db.session.query(Task).filter(
                Task.process_id == process_id,
                Task.task_id == node.get('task_id'),
            ).first()
            if not node.get('method_kwargs'):
                node['method_kwargs'] = {}
            if not node.get('task_config'):
                node['task_config'] = {}
            task = TaskSchema().load(node)
            if task_obj:
                db.session.query(Task).filter(
                    Task.process_id == process_id,
                    Task.task_id == node.get('task_id'),
                ).update(task)
            else:
                task_obj = Task(**task)
                db.session.add(task_obj)
            db.session.commit()

        return generate_response(data={'process_id': process_obj.id})

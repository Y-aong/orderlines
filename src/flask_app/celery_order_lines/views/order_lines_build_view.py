# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_build_view.py
# Time       ：2023/3/12 13:22
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import json

from flask import request

from flask_restful import Resource

from flask_app.celery_order_lines.models.base_model import db
from flask_app.celery_order_lines.models.order_line_models import ProcessModel, TaskModel
from flask_app.celery_order_lines.schema.order_lines_schema import ProcessSchema, TaskSchema
from flask_app.public.response import generate_response


class OrderLinesBuildView(Resource):
    url = '/build/process'

    def __init__(self):
        self.form_data = request.json

    def post(self):
        process_info = self.form_data.get('process_info')
        node_info = self.form_data.get('process_node')
        process_id = process_info.get('process_id')
        # 生成process
        process = ProcessSchema().load(process_info)
        process_obj = db.session.query(ProcessModel).filter(ProcessModel.process_id == process_id).first()
        if process_obj:
            db.session.query(ProcessModel).filter(ProcessModel.process_id == process_id).update(process)
        else:
            process_obj = ProcessModel(**process)
            db.session.add(process_obj)
        db.session.commit()
        # 生成task
        for node in node_info:
            node['process_id'] = process_id
            method_kwargs = json.dumps(node.get('method_kwargs')) if node.get('method_kwargs') else '{}'
            task_config = json.dumps(node.get('task_config')) if node.get('task_config') else '{}'
            node['task_config'] = task_config
            task_obj = db.session.query(TaskModel).filter(
                TaskModel.process_id == process_id,
                TaskModel.task_name == node.get('task_name'),
                TaskModel.method_kwargs == method_kwargs
            ).first()
            if not node.get('method_kwargs'):
                node['method_kwargs'] = {}
            task = TaskSchema().load(node)
            if task_obj:
                db.session.query(TaskModel).filter(
                    TaskModel.process_id == process_id,
                    TaskModel.task_name == node.get('task_name'),
                    TaskModel.task_module == node.get('task_module')
                ).update(task)
            else:
                task_obj = TaskModel(**task)
                db.session.add(task_obj)
            db.session.commit()

        return generate_response(data={'process_id': process_obj.id})

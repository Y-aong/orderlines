# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : flow_task_config_view.py
# Time       ：2023/9/16 15:25
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    给前端存储流程图用
"""
from flask import request
from flask_restful import Resource

from public.base_response import generate_response
from public.mongo_utils import MongoDBUtil


class FlowTaskConfigView(Resource):
    url = '/flow_task_config'

    def __init__(self):
        if request.method == 'GET' or request.method == 'DELETE':
            self.form_data: dict = request.args
        else:
            self.form_data: dict = request.json

    @property
    def mongo(self):
        return MongoDBUtil('flow_task_data')

    def get(self):
        process_id = self.form_data.get('process_id')
        task_id = self.form_data.get('task_id')
        flow_task_data = self.mongo.get_value(process_id, task_id)
        if flow_task_data and '_id' in flow_task_data:
            flow_task_data.pop('_id')
            return generate_response(flow_task_data)
        else:
            return generate_response({})

    def post(self):
        process_id = self.form_data.pop('process_id')
        task_id = self.form_data.pop('task_id')
        self.mongo.set_value(process_id, task_id, **self.form_data)
        return generate_response()

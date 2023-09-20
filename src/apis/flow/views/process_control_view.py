# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : process_control_view.py
# Time       ：2023/9/20 18:22
# Author     ：YangYong
# version    ：python 3.10
# Description：
    获取流程控制后续节点
"""
from flask import request
from flask_restful import Resource

from public.base_response import generate_response
from public.mongo_utils import MongoDBUtil


class ProcessControlView(Resource):
    url = '/process_control'

    def __init__(self):
        self.mongo = MongoDBUtil('flow_data')
        self.form_data = request.args

    @staticmethod
    def get_task_name(source_task_id: str, nodes: list):
        for node in nodes:
            if node.get('id') == source_task_id:
                return node.get('text').get('value')
        return None

    def post(self):
        task_id = self.form_data.get('task_id')
        filter_ = {'process_id': self.form_data.get('process_id')}
        flow_data = self.mongo.collection.find_one(filter_)
        if '_id' in flow_data:
            flow_data.pop('_id')
        graph_data = flow_data.get('graphData')
        nodes = graph_data.get('nodes')
        edges = graph_data.get('edges')
        task_id_options = list()

        for edge in edges:
            if edge.get('sourceNodeId') == task_id:
                target_id = edge.get('targetNodeId')
                task_ids = {
                    'label': self.get_task_name(target_id, nodes),
                    'value': target_id
                }
                task_id_options.append(task_ids)
        return generate_response(task_id_options)

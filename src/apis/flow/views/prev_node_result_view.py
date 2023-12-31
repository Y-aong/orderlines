# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : prev_node_result_view.py
# Time       ：2023/9/21 15:54
# Author     ：YangYong
# version    ：python 3.10
# Description：
    获取上个节点的返回值信息
"""
from flask import request
from flask_restful import Resource

from apis.orderlines.models import Task
from apis.orderlines.schema.task_schema import TaskSchema
from public.api_handle_exception import handle_api_error
from public.base_model import db
from public.base_response import generate_response
from public.logger import logger
from public.mongo_utils import MongoDBUtil


class PrevNodeResultView(Resource):
    url = '/prev_node_result'

    def __init__(self):
        self.form_data = request.args
        self.mongo = MongoDBUtil('flow_data')

    def get_prev_id(self):
        filter_ = {'process_id': self.form_data.get('process_id')}
        flow_data = self.mongo.collection.find_one(filter_)
        if '_id' in flow_data:
            flow_data.pop('_id')
        graph_data = flow_data.get('graphData')
        nodes = graph_data.get('nodes')
        edges = graph_data.get('edges')

        task_nodes = list()
        for node in nodes:
            item = {}
            task_id = node.get('id')
            task_name = node.get('text').get('value')
            item['task_id'] = task_id
            item['task_name'] = task_name
            prev_id = list()
            next_id = list()
            for edge in edges:
                if edge.get('sourceNodeId') == task_id:
                    next_id.append(edge.get('targetNodeId'))

                if edge.get('targetNodeId') == task_id:
                    prev_id.append(edge.get('sourceNodeId'))

            item['prev_id'] = prev_id
            item['next_id'] = next_id
            item['task_id'] = task_id
            task_nodes.append(item)
        task_id = self.form_data.get('task_id')

        for node in task_nodes:
            if task_id in node.get('next_id'):
                return node.get('task_id')
        return None

    @handle_api_error
    def get(self):
        try:
            prev_id = self.get_prev_id()
            obj = db.session.query(Task).filter(Task.task_id == prev_id).first()
            task_info = TaskSchema().dump(obj)
            result_config = task_info.get('result_config')
            result_config_options = list()
            if isinstance(result_config, dict):
                result_config = [result_config]
            for item in result_config:
                result_config_options.append({
                    'label': item.get('result_key'),
                    'value': item.get('variable_key'),
                })
            pre_task_config = [{'label': task_info.get('task_name'), 'value': task_info.get('task_id')}]
            result = {
                'result_config_options': result_config_options,
                'pre_task_config': pre_task_config
            }
            return generate_response(result)
        except Exception as e:
            logger.error(f'获取前置节点返回值失败:{e}')
            raise ValueError(f'获取前置节点返回值失败')

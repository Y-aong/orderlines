# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : flow_save_view.py
# Time       ：2023/9/19 16:29
# Author     ：YangYong
# version    ：python 3.10
# Description：
    保存流程图数据
"""
from flask import request

from flask_restful import Resource

from apis.orderlines.models import Task
from public.base_model import db
from public.base_response import generate_response
from public.mongo_utils import MongoDBUtil


class FlowSaveView(Resource):
    url = '/flow_save'

    def __init__(self):
        self.form_data = request.json
        self.mongo = MongoDBUtil('flow_data')

    def post(self):
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

            item['prev_id'] = ','.join(prev_id) if prev_id else None
            item['next_id'] = ','.join(next_id) if next_id else None
            task_nodes.append(item)

        print(task_nodes)
        for task_node in task_nodes:
            update_data = {
                'prev_id': task_node.get('prev_id'),
                'next_id': task_node.get('next_id'),
            }
            with db.auto_commit():
                db.session.query(Task).filter(
                    Task.task_id == task_node.get('task_id'),
                    Task.active == 1
                ).update(update_data)
        return generate_response('流程保存成功')

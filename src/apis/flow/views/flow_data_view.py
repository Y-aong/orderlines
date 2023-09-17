# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : flow_data_view.py
# Time       ：2023/9/17 11:30
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程图数据
"""
from flask import request
from flask_restful import Resource

from orderlines.utils.exceptions import VariableException
from public.base_response import generate_response
from public.logger import logger
from public.mongo_utils import MongoDBUtil


class FlowDataView(Resource):
    url = '/flow_data'

    def __init__(self):
        self.mongo = MongoDBUtil('flow_data')
        if request.method == 'GET' or request.method == 'DELETE':
            self.form_data: dict = request.args
        else:
            self.form_data: dict = request.json

    def get(self):
        try:
            filter_ = {'process_id': self.form_data.get('process_id')}
            flow_data = self.mongo.collection.find_one(filter_)
            if '_id' in flow_data:
                flow_data.pop('_id')
            return generate_response(flow_data)
        except Exception as e:
            logger.info(f'当前没有流程数据::{e}')
            return generate_response({})

    def post(self):
        filter_ = {'process_id': self.form_data.get('process_id')}
        obj = self.mongo.collection.find_one(filter_)
        if obj:
            self.mongo.collection.update_one(filter=filter_, update={'$set': self.form_data}, upsert=True)
        else:
            self.mongo.collection.insert_one(self.form_data)
        return generate_response(message='流程图数据设置成功')

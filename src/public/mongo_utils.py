# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mongo_utils.py
# Time       ：2023/8/21 11:54
# Author     ：YangYong
# version    ：python 3.10
# Description：
    mongo db utils
"""
import json
from typing import Any

import pandas as pd
import pymongo

from conf.config import Mongo
from orderlines.utils.exceptions import VariableException
from public.logger import logger


class MongoDBUtil:
    def __init__(self, collection=None):
        self.mongo = pymongo.MongoClient(host=Mongo.host, port=Mongo.port)
        self.db = self.mongo[Mongo.db]
        if not collection:
            collection = Mongo.collection
        self.collection = self.db[collection]

    def set_value(self, process_id: str, task_id: str, **kwargs):
        try:
            filter_ = {'process_id': process_id, 'task_id': task_id}
            obj = self.collection.find_one(filter_)
            if obj:
                self.collection.update_one(filter=filter_, update={'$set': kwargs}, upsert=True)
            else:
                data = {
                    'process_id': process_id,
                    'task_id': task_id,
                }
                data.update(kwargs)
                self.collection.insert_one(data)
        except Exception as e:
            raise VariableException(f'mongo db set value error. error info is {e}')

    def get_value(self, process_id: str, task_id: str):
        try:
            filter_ = {'process_id': process_id, 'task_id': task_id}
            return self.collection.find_one(filter_)
        except Exception as e:
            raise VariableException(f'mongo db get value error. error info is {e}')

    def set_variable_value(self, process_instance_id: str, variable_key: str, variable_value: Any):
        """mongodb set value"""
        try:
            if isinstance(variable_value, pd.DataFrame):
                variable_value = variable_value.to_json()
            data = {
                'process_instance_id': process_instance_id,
                'variable_key': variable_key,
                'variable_value': variable_value
            }
            self.collection.insert_one(data)
        except Exception as e:
            logger.error(f'mongo db set value error. error info is {e}')
            raise VariableException(f'mongo db set value error. error info is {e}')

    def get_variable_value(self, process_instance_id: str, variable_key: str, variable_type: str):
        """mongodb get value"""
        try:
            search_key = {
                'process_instance_id': process_instance_id,
                'variable_key': variable_key
            }
            variable = self.collection.find_one(search_key)
            variable_value = variable.get('variable_value')
            if variable_type.lower() == 'str':
                return str(variable_value)
            elif variable_type.lower() == 'int':
                return int(variable_value)
            elif variable_type.lower() == 'float':
                return float(variable_value)
            elif variable_type.lower() == 'dict' or variable_type.lower() == 'list':
                return variable_value
            elif variable_type.lower() == 'pd.dataframe':
                if not isinstance(variable_value, dict) or not isinstance(variable_value, list):
                    return pd.DataFrame(json.loads(variable_value))
                else:
                    return pd.DataFrame(variable_value)
            elif variable_type.lower() == 'none':
                return None
        except Exception as e:
            logger.error(f'mongo db get value error. error info is {e}')
            raise VariableException(f'mongo db get value error. error info is {e}')

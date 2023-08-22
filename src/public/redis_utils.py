# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : redis_utils.py
# Time       ：2023/8/14 10:31
# Author     ：YangYong
# version    ：python 3.10
# Description：
    redis 工具类
    redis utils
"""
import json
from typing import Any, List

import pandas as pd
import redis

from conf.config import Redis


class RedisUtils:
    def __init__(self, name=None):
        self.redis = redis.Redis(host=Redis.host, port=Redis.port, db=Redis.db)
        self.name = name

    def len(self) -> int:
        """获取队列长度"""
        return self.redis.llen(self.name)

    def index(self, index: int) -> dict:
        """获取指定位置的队列元素"""
        value = self.redis.lindex(self.name, index)
        return json.loads(value.decode('utf-8')) if value else {}, value

    def rpop(self) -> dict:
        """从队列右侧弹出元素"""
        value = self.redis.rpop(self.name)
        return json.loads(value.decode('utf-8')) if value else {}

    def remove(self, item: dict) -> None:
        """删除元素"""
        self.redis.lrem(self.name, 0, item)

    def lpush(self, item: Any) -> None:
        """左侧添加元素"""
        if isinstance(item, dict) or isinstance(item, list):
            item = json.dumps(item)
        self.redis.lpush(self.name, item)

    def get_all_items(self, clear=False) -> List[dict]:
        """
        获取redis list中所有元素
        @return:
        """
        all_items = []
        queue_length = self.len()
        if not queue_length:
            return all_items
        for i in range(queue_length)[::-1]:
            if clear:
                item = self.rpop()
            else:
                item, original_value = self.index(i)
            all_items.append(item)
        return all_items

    def hset(self, process_instance_id: str, variable_name: str, variable_value: dict):
        if isinstance(variable_value, dict):
            variable_value = json.dumps(variable_value)
        elif isinstance(variable_value, list):
            variable_value = json.dumps(variable_value)
        elif isinstance(variable_value, pd.DataFrame):
            variable_value = variable_value.to_json()

        if not isinstance(variable_value, str):
            raise ValueError('please check variable value, now only support str,dict,list,pd.DataFrame')

        self.redis.hset(process_instance_id, variable_name, variable_value)

    def hget(self, process_instance_id: str, variable_name: str, variable_type: str):
        """获取变量值"""
        variable_value = self.redis.hget(process_instance_id, variable_name)
        if variable_type.lower() == 'str':
            return variable_value.decode('utf-8')
        elif variable_type.lower() == 'int':
            return int(variable_value.decode('utf-8'))
        elif variable_type.lower() == 'float':
            return float(variable_value.decode('utf-8'))
        elif variable_type.lower() == 'dict' or variable_type.lower() == 'list':
            return json.loads(variable_value.decode('utf-8'))
        elif variable_type.lower() == 'pd.dataframe':
            return pd.DataFrame(json.loads(variable_value.decode('utf-8')))
        elif variable_type.lower() == 'none':
            return None
        else:
            raise ValueError('variable not support variable type')

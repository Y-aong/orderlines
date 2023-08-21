# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_variable_cache.py
# Time       ：2023/8/21 13:54
# Author     ：YangYong
# version    ：python 3.10
# Description：
    测试变量缓存
"""
import pandas as pd

from public.mongo_utils import MongoDBUtil
from public.redis_utils import RedisUtils


def test_redis_variable_cache():
    process_instance_id = '1001'
    variable_key = 'test001'
    variable_value = '100'
    redis = RedisUtils()
    redis.hset(process_instance_id, variable_key, variable_value)

    value = redis.hget(process_instance_id, variable_key, 'str')
    assert value == '100'

    value = redis.hget(process_instance_id, variable_key, 'int')
    assert value == 100

    variable_key = 'test002'
    variable_value = {'name': 'zs'}
    redis.hset(process_instance_id, variable_key, variable_value)
    value = redis.hget(process_instance_id, variable_key, 'dict')
    assert value == {'name': 'zs'}

    variable_key = 'test003'
    variable_value = ['name', 'age']
    redis.hset(process_instance_id, variable_key, variable_value)
    value = redis.hget(process_instance_id, variable_key, 'list')
    assert value == ['name', 'age']

    variable_key = 'test004'
    data = {'col1': [1, 2], 'col2': [3, 4]}
    variable_value = pd.DataFrame(data)
    redis.hset(process_instance_id, variable_key, variable_value)
    value = redis.hget(process_instance_id, variable_key, 'pd.dataframe')
    assert isinstance(value, pd.DataFrame)


def test_mongodb_variable_cache():
    process_instance_id = '1001'
    variable_key = 'test001'
    variable_value = '100'
    mongo = MongoDBUtil()
    mongo.set_value(process_instance_id, variable_key, variable_value)

    value = mongo.get_value(process_instance_id, variable_key, 'str')
    assert value == '100'

    value = mongo.get_value(process_instance_id, variable_key, 'int')
    assert value == 100

    variable_key = 'test002'
    variable_value = {'name': 'zs'}
    mongo.set_value(process_instance_id, variable_key, variable_value)
    value = mongo.get_value(process_instance_id, variable_key, 'dict')
    assert value == {'name': 'zs'}

    variable_key = 'test003'
    variable_value = ['name', 'age']
    mongo.set_value(process_instance_id, variable_key, variable_value)
    value = mongo.get_value(process_instance_id, variable_key, 'list')
    assert value == ['name', 'age']

    variable_key = 'test004'
    data = {'col1': [1, 2], 'col2': [3, 4]}
    variable_value = pd.DataFrame(data)
    mongo.set_value(process_instance_id, variable_key, variable_value)
    value = mongo.get_value(process_instance_id, variable_key, 'pd.dataframe')
    assert isinstance(value, pd.DataFrame)

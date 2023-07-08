# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : utils.py
# Time       ：2023/1/29 22:24
# Author     ：Y-aong
# version    ：python 3.7
# Description：order_line工具类
"""
import json
from typing import MutableMapping

from order_lines.utils.order_lines_types import is_string, is_dict_like


def get_current_node(task_id, process_node):
    """
    根据当前任务id获取当前正在运行的任务
    :return:当前的任务信息
    """
    for node in process_node:
        if node.get('task_id') == task_id:
            return node
    raise AttributeError(f'根据task id {task_id} 找不到任务节点')


def get_variable_value(variable_value, variable_type):
    if not variable_value:
        return None
    if variable_type == 'int':
        return int(variable_value)
    elif variable_type == 'str':
        return str(variable_value)
    elif variable_type == 'float':
        return float(variable_value)
    elif variable_type == 'bool':
        return bool(variable_value)
    elif variable_type == 'json':
        return json.dumps(variable_value)
    elif variable_type in 'dict':
        return json.loads(variable_value)
    else:
        return None


def normalize(string, ignore=(), caseless=True, spaceless=True):
    """根据给定的规范规范化给定的字符串"""
    empty = '' if is_string(string) else b''
    if isinstance(ignore, bytes):
        # Iterating bytes in Python3 yields integers.
        ignore = [bytes([i]) for i in ignore]
    if spaceless:
        string = empty.join(string.split())
    if caseless:
        string = string.lower()
        ignore = [i.lower() for i in ignore]
    # both if statements below enhance performance a little
    if ignore:
        for ign in ignore:
            if ign in string:
                string = string.replace(ign, empty)
    return string

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : api_utils.py
# Time       ：2023/1/29 22:24
# Author     ：Y-aong
# version    ：python 3.7
# Description：order_line util
"""
import inspect
import json
from typing import List, Any


def get_current_node(task_id: str, task_nodes: List[dict]) -> dict:
    """
    根据任务id获取当前运行的任务
    Obtain the currently running task based on the task id
    """
    for node in task_nodes:
        if node.get('task_id') == task_id:
            return node
    raise AttributeError(f'use task id {task_id} The task node cannot be found')


def get_variable_value(variable_value: Any, variable_type: str) -> Any:
    """按类型获取变量值. get variable value by type"""
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


def get_method_param_annotation(method) -> tuple:
    """
    获取方法的参数类型注解
    Gets the parameter type annotation for the method
    @param method: method
    @return: flag, param_annotation
    flag is use pydantic
    """
    sig = inspect.signature(method)
    parameters = sig.parameters
    arg_keys = tuple(arg for arg in parameters.keys() if arg != 'self')
    if len(arg_keys) == 1:
        for arg_name in arg_keys:
            return True, parameters[arg_name].annotation
    return False, tuple(parameters.get(arg) for arg in parameters.keys() if arg != 'self')

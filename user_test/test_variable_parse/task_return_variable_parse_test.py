# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_return_variable_parse_test.py
# Time       ：2023/8/12 17:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试任务返回值解析
"""
import uuid

from orderlines.variable.common_task_strategy import CommonTaskVariableStrategy


def task_result_variable_parse():
    variable_config = [
        {
            'variable_key': 'add_result',
            'variable_desc': 'add函数的返回值',
            'variable_type': 'int',
        }
    ]
    task_result = {
        'add_value': 108,
        'status': 'SUCCESS'
    }

    node_result_config = {
        "result_key": "add_value",
        "variable_key": "${add_result}"
    }
    process_instance_id = str(uuid.uuid1().hex)
    task_variable = CommonTaskVariableStrategy(process_instance_id)
    task_result = task_variable.handle_task_result(variable_config, task_result, node_result_config)
    print(task_result)


task_result_variable_parse()

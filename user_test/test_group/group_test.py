# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_test.py
# Time       ：2023/2/26 22:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试任务组
"""
from order_lines.enter_point import OrderLines

data = [
    {
        "task_id": 1001,
        "task_name": "开始节点",
        "method_name": 'start',
        "task_type": "start",
        "method_kwargs": None,
        "prev_id": None,
        "next_id": 1002,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    },
    {
        "task_id": 1002,
        "task_name": "任务组",
        "method_name": "task_group",
        "task_type": "group",
        "method_kwargs": {
            "group_ids": [1003, 1004]
        },
        "prev_id": 1001,
        "next_id": 1005,
        "task_config": None,
        "task_module": "Group",
        "desc": None
    },
    {
        "task_id": 1003,
        "task_name": "减法",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": 10,
            "b": 12
        },
        "result": [
            {
                "subtraction_value": "${subtraction_value}+1",
                "variable_type": "int",
                "variable_desc": "subtraction函数的返回值"
            }
        ],
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": 1004,
        "task_name": "减法1",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": "${subtraction_value}",
            "b": 12
        },
        "prev_id": 1002,
        "next_id": 1005,
        "result": [
            {
                "subtraction_value": "${return_value}",
                "variable_type": "int",
                "variable_desc": "subtraction函数的返回值"
            }
        ],
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": 1005,
        "task_name": "结束节点",
        "method_name": 'end',
        "task_type": "end",
        "method_kwargs": None,
        "prev_id": 1002,
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]
process_info = {
    'process_id': '1004',
    'process_name': 'test_group',
    "creator": "blue",
    "updater": None,
}

if __name__ == '__main__':
    OrderLines(process_info, data).run()

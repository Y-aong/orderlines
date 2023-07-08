# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : parallel_with_task_test.py
# Time       ：2023/3/3 22:14
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试并行任务，不声明任务组，让框架自己寻找
"""
from order_lines.enter_point import OrderLines

nodes = [
    {
        "task_id": 1000,
        "task_name": "start",
        "method_name": "start",
        "task_type": "start",
        "method_kwargs": {},
        "prev_id": None,
        "next_id": 1001,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    },
    {
        "task_id": 1001,
        "task_name": "并行网关",
        "method_name": "parallel_task",
        "task_type": "parallel",
        "method_kwargs": {
            "parallel_task_ids": [1002, 1005]
        },
        "prev_id": 1001,
        "next_id": 1007,
        "task_config": {
            'runner': 'gevent'
        },
        "task_module": "Parallel",
        "desc": None
    },
    {
        "task_id": 1002,
        "task_name": "任务组1",
        "method_name": "task_group",
        "task_type": "group",
        "method_kwargs": {
            "group_ids": [1003, 1004]
        },
        "task_config": None,
        "task_module": "Group",
        "desc": None
    },
    {
        "task_id": 1003,
        "task_name": "add1",
        "method_name": "test_add",
        "task_type": "common",
        "method_kwargs": {
            "a": 1,
            "b": 123143
        },
        "task_config": None,
        "task_module": "Test",
        "result": [
            {
                "add_value": "${add_value}+1",
                "variable_type": "int",
                "variable_desc": "add函数的返回值"
            }
        ],
        "desc": None
    },
    {
        "task_id": 1004,
        "task_name": "subtraction1",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": "${add_value}",
            "b": 123123
        },
        "task_config": None,
        "task_module": "Test",
        "result": [
            {
                "subtraction_value": "${return_value}",
                "variable_type": "int",
                "variable_desc": "subtraction函数的返回值"
            }
        ],
        "desc": None
    },
    {
        "task_id": 1005,
        "task_name": "任务组2",
        "method_name": "task_group",
        "task_type": "group",
        "method_kwargs": {
            "group_ids": [1006]
        },
        "task_config": None,
        "task_module": "Group",
        "desc": None
    },
    {
        "task_id": 1006,
        "task_name": "减法",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": 10,
            "b": 12
        },
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": 1007,
        "task_name": "end",
        "method_name": "end",
        "task_type": "end",
        "method_kwargs": {},
        "prev_id": 1001,
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]
process_info = {
    'process_id': '1005',
    'process_name': 'test_parallel_with_group',
    "creator": "blue",
    "updater": None,
}
if __name__ == '__main__':
    OrderLines(process_info, nodes).run()

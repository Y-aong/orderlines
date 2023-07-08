# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_return_test.py
# Time       ：2023/2/25 16:36
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试流程控制——返回值
"""
from order_lines.enter_point import OrderLines

nodes = [
    {
        "task_id": 1011,
        "task_name": "start",
        "method_name": "start",
        "task_type": "start",
        "method_kwargs": None,
        "prev_id": None,
        "next_id": 1012,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    },
    {
        "task_id": 1012,
        "task_name": "add",
        "method_name": "test_add",
        "task_type": "common",
        "method_kwargs": {
            "a": 2,
            "b": 786
        },
        "prev_id": 1011,
        "next_id": 1013,
        "task_config": {
            "task_strategy": 'skip'
        },
        "task_module": "Test",
        "result": [
            {
                "add_value": "${add_value}",
                "variable_type": "int",
                "variable_desc": "add函数的返回值"
            }
        ],
        "desc": None
    },

    {
        "task_id": 1013,
        "task_name": "process_control",
        "method_name": "process_control",
        "task_type": "process_control",
        "method_kwargs": {
            "conditions": [
                {
                    'A': [{'condition': 1, 'target': "${add_value}", 'sign': '='},
                          {'condition': 1, 'target': 3, 'sign': '>'}]
                },
                {
                    'B': [{'condition': 2, 'target': "${add_value}", 'sign': '<'},
                          {'condition': 3, 'target': 3, 'sign': '='}]
                }
            ],
            "expression": {
                'A': {'task_id': 1014},
                'B': {'task_id': 1015}
            },
            "prev_id": 1012,
            "next_id": None,
            "task_config": None,
            "task_module": "ProcessControl",
            "desc": None
        },
        "prev_id": 1012,
        "next_id": None,
        "task_config": None,
        "task_module": "ProcessControl",
        "desc": None
    },
    {
        "task_id": 1014,
        "task_name": "add",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": 2,
            "b": 712
        },
        "prev_id": 1013,
        "next_id": 1016,
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": 1015,
        "task_name": "add",
        "method_name": "test_add",
        "task_type": "common",
        "method_kwargs": {
            "a": 2,
            "b": 78
        },
        "prev_id": 1013,
        "next_id": 1016,
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": 1016,
        "task_name": "end",
        "method_name": "end",
        "task_type": "end",
        "method_kwargs": None,
        "prev_id": [1014, 1015],
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]

process_info = {
    "process_id": "1007",
    "process_name": "test_process_return",
    "creator": "blue",
}
if __name__ == '__main__':
    OrderLines(process_info, nodes).run()

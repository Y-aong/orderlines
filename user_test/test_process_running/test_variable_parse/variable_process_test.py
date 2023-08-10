# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_process_test.py
# Time       ：2023/2/6 21:29
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from orderlines.app import OrderLines

data = [
    {
        "task_id": "1001",
        "task_name": "start",
        "method_name": "start",
        "task_type": "start",
        "method_kwargs": {},
        "prev_id": None,
        "next_id": "1002",
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    },
    {
        "task_id": "1002",
        "task_name": "add",
        "method_name": "test_add",
        "task_type": "common",
        "method_kwargs": {
            "a": 1,
            "b": 123143
        },
        "prev_id": "1001",
        "next_id": "1003",
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
        "task_id": "1003",
        "task_name": "subtraction",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": "${add_value}",
            "b": 123123
        },
        "prev_id": "1002",
        "next_id": "1004",
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
        "task_id": "1004",
        "task_name": "end",
        "method_name": "end",
        "task_type": "end",
        "method_kwargs": {},
        "prev_id": "1003",
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]

process_info = {
    "process_id": "1003",
    "process_name": "test_variable1",
    "creator": "blue",
}

if __name__ == '__main__':
    orderlines = OrderLines()
    orderlines.clear_db()
    orderlines.start(process_info=process_info, task_nodes=data)

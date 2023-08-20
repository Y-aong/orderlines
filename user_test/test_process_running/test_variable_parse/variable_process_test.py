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


def test_variable_process():
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
            "module_version": "1.0.0.1",
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
            "module_version": "1.0.0.1",
            "result_config":
                {
                    "result_key": "add_value",
                    "variable_key": "${add_result}",
                },
            "desc": None
        },
        {
            "task_id": "1003",
            "task_name": "subtraction",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": "${add_result}",
                "b": 123123
            },
            "prev_id": "1002",
            "next_id": "1004",
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "result_config": [

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
            "module_version": "1.0.0.1",
            "desc": None
        }
    ]

    process_info = {
        "process_id": "1003",
        "process_name": "test_variable1",
        "creator": "blue",
    }
    variable = [
        {
            "variable_key": "add_result",
            "variable_type": "int",
            "variable_desc": "add函数的返回值"
        }
    ]

    orderlines = OrderLines()
    orderlines.start(process_info=process_info, task_nodes=data, variable=variable, clear_db=True)


if __name__ == '__main__':
    test_variable_process()

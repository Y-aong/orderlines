# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : parallel_with_task_test.py
# Time       ：2023/3/3 22:14
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试并行任务，不声明任务组，让框架自己寻找
"""
from orderlines.app import OrderLines


def test_parallel_with_test():
    data = [
        {
            "task_id": "1000",
            "task_name": "start",
            "method_name": "start",
            "task_type": "start",
            "method_kwargs": {},
            "prev_id": None,
            "next_id": "1001",
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1001",
            "task_name": "并行网关",
            "method_name": "parallel_task",
            "task_type": "parallel",
            "method_kwargs": {
                "parallel_task_ids": ["1002", "1005"]
            },
            "prev_id": "1001",
            "next_id": "1007",
            "task_config": {
                'runner': 'gevent'
            },
            "task_module": "Parallel",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1002",
            "task_name": "任务组1",
            "method_name": "task_group",
            "task_type": "group",
            "method_kwargs": {
                "group_ids": ["1003", "1004"]
            },
            "task_config": None,
            "task_module": "Group",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1003",
            "task_name": "add1",
            "method_name": "test_add",
            "task_type": "common",
            "method_kwargs": {
                "a": 1,
                "b": 123143
            },
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
            "task_id": "1004",
            "task_name": "subtraction1",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": 1231,
                "b": 123123
            },
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "result_config": {
                "result_key": "subtraction_value",
                "variable_key": "${subtraction_result}",
            },
            "desc": None
        },
        {
            "task_id": "1005",
            "task_name": "任务组2",
            "method_name": "task_group",
            "task_type": "group",
            "method_kwargs": {
                "group_ids": ["1006"]
            },
            "task_config": None,
            "task_module": "Group",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1006",
            "task_name": "减法",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": 10,
                "b": 12
            },
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1007",
            "task_name": "end",
            "method_name": "end",
            "task_type": "end",
            "method_kwargs": {},
            "prev_id": "1001",
            "next_id": None,
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        }
    ]
    process_info = {
        'process_id': '1005',
        'process_name': 'test_parallel_with_group',
        "creator": "blue",
        "updater": None,
    }
    variable = [
        {
            "variable_key": "subtraction_result",
            "variable_type": "int",
            "variable_desc": "减法的返回值"
        },
        {
            "variable_key": "add_result",
            "variable_type": "int",
            "variable_desc": "加法的返回值"
        }
    ]

    orderlines = OrderLines()
    orderlines.start(process_info=process_info, task_nodes=data, variable=variable, clear_db=True)


if __name__ == '__main__':
    test_parallel_with_test()

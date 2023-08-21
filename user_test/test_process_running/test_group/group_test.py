# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_test.py
# Time       ：2023/2/26 22:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试任务组
"""

from orderlines.app import OrderLines


def group_task_test():
    data = [
        {
            "task_id": "1001",
            "task_name": "开始节点",
            "method_name": 'start',
            "task_type": "start",
            "method_kwargs": None,
            "prev_id": None,
            "next_id": "1002",
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1002",
            "task_name": "任务组",
            "method_name": "task_group",
            "task_type": "group",
            "method_kwargs": {
                "group_ids": ["1003", "1004"]
            },
            "prev_id": "1001",
            "next_id": "1005",
            "task_config": None,
            "task_module": "Group",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1003",
            "task_name": "减法",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": 10,
                "b": 12
            },
            "result_config": {
                "result_key": "subtraction_value",
                "variable_key": "${add_result}",
            },
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1004",
            "task_name": "减法1",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": "${add_result}",
                "b": 12
            },
            "prev_id": "1002",
            "next_id": "1005",
            "result_config": {
                "result_key": "subtraction_value",
                "variable_key": "${subtraction_result}",
            },
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1005",
            "task_name": "结束节点",
            "method_name": 'end',
            "task_type": "end",
            "method_kwargs": None,
            "prev_id": "1002",
            "next_id": None,
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        }
    ]
    process_info = {
        'process_id': '1004',
        'process_name': 'test_group',
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
    group_task_test()

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_return_test.py
# Time       ：2023/2/25 16:36
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试流程控制——返回值
"""
from orderlines.app import OrderLines


def process_control_return_test():
    data = [
        {
            "task_id": "1011",
            "task_name": "start",
            "method_name": "start",
            "task_type": "start",
            "method_kwargs": None,
            "prev_id": None,
            "next_id": "1012",
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1012",
            "task_name": "add",
            "method_name": "test_add",
            "task_type": "common",
            "method_kwargs": {
                "a": 2,
                "b": 786
            },
            "prev_id": "1011",
            "next_id": "1013",
            "task_config": {
                "task_strategy": 'skip'
            },
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "result_config": {
                "result_key": "add_value",
                "variable_key": "${add_result}",
            },
            "desc": None
        },

        {
            "task_id": "1013",
            "task_name": "process_control",
            "method_name": "process_control",
            "task_type": "process_control",
            "method_kwargs": {
                "pc_type": "result",
                "conditions": [
                    {
                        'task_id': '1014',
                        'condition': [
                            {'sign': '=', 'target': 788, 'condition': 1},
                            {'sign': '>', 'target': 3, 'condition': 1}
                        ]
                    },
                    {
                        'task_id': '1015',
                        'condition': [
                            {'sign': '<', 'target': 788, 'condition': 2},
                            {'sign': '=', 'target': 3, 'condition': 3}
                        ]
                    }
                ],

            },
            "prev_id": "1012",
            "next_id": None,
            "task_config": None,
            "task_module": "ProcessControl",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1014",
            "task_name": "add",
            "method_name": "test_subtraction",
            "task_type": "common",
            "method_kwargs": {
                "a": 2,
                "b": 712
            },
            "prev_id": "1013",
            "next_id": "1016",
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1015",
            "task_name": "add",
            "method_name": "test_add",
            "task_type": "common",
            "method_kwargs": {
                "a": 2,
                "b": 78
            },
            "prev_id": "1013",
            "next_id": "1016",
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1016",
            "task_name": "end",
            "method_name": "end",
            "task_type": "end",
            "method_kwargs": None,
            "prev_id": ["1014", "1015"],
            "next_id": None,
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        }
    ]

    process_info = {
        "process_id": "1007",
        "process_name": "test_process_return",
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
    process_control_return_test()

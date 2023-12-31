# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_timeout_test.py
# Time       ：2023/3/11 17:05
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试流程超时,但是不建议配置流程操作，一般配置任务超时就可以了
"""
from orderlines.app import OrderLines


def process_timeout_test():
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
            "desc": None
        },
        {
            "task_id": "1002",
            "task_name": "加法",
            "method_name": "test_add",
            "task_type": "common",
            "method_kwargs": {
                "a": 1,
                "b": 2
            },
            "prev_id": "1001",
            "next_id": "1003",
            "task_config": {
                'timeout': 3
            },
            "task_module": "Test",
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
            "prev_id": "1002",
            "next_id": "1004",
            "task_config": None,
            "task_module": "Test",
            "desc": None
        },
        {
            "task_id": "1004",
            "task_name": "结束节点",
            "method_name": 'end',
            "task_type": "end",
            "method_kwargs": None,
            "prev_id": "1003",
            "next_id": None,
            "task_config": None,
            "task_module": "BuiltIn",
            "desc": None
        }
    ]
    process_info = {
        'process_id': '1009',
        'process_name': 'test_process_timeout',
        "creator": "blue",
        "updater": None,
        "process_config": {
            "timeout": 1
        }
    }

    OrderLines().start(process_info=process_info, task_nodes=data, clear_db=True)


if __name__ == '__main__':
    process_timeout_test()

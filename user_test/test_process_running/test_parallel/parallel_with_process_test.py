# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : parallel_with_process_test.py
# Time       ：2023/3/11 16:59
# Author     ：Y-aong
# version    ：python 3.7
# Description：使用进程方式运行任务组,任务组中运行的是计算密集型数据
"""
from order_lines.app import OrderLines

nodes = [
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
        "desc": None
    },
    {
        "task_id": "1001",
        "task_name": "并行网关",
        "method_name": "parallel_task",
        "task_type": "parallel",
        "method_kwargs": {
            "parallel_task_ids": ["1002", "1004"]
        },
        "prev_id": "1001",
        "next_id": "1006",
        "task_config": {
            'runner': 'process'
        },
        "task_module": "Parallel",
        "desc": None
    },
    {
        "task_id": "1002",
        "task_name": "任务组1",
        "method_name": "task_group",
        "task_type": "group",
        "method_kwargs": {
            "group_ids": ["1003"]
        },
        "prev_id": "1001",
        "next_id": "1006",
        "task_config": None,
        "task_module": "Group",
        "desc": None
    },
    {
        "task_id": "1003",
        "task_name": "减法",
        "method_name": "test_subtraction",
        "task_type": "common",
        "method_kwargs": {
            "a": 10,
            "b": 123
        },
        "task_config": None,
        "task_module": "Test",
        "desc": None
    },
    {
        "task_id": "1004",
        "task_name": "任务组2",
        "method_name": "task_group",
        "task_type": "group",
        "method_kwargs": {
            "group_ids": ["1005"]
        },
        "prev_id": "1001",
        "next_id": "1006",
        "task_config": None,
        "task_module": "Group",
        "desc": None
    },
    {
        "task_id": "1005",
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
        "task_id": "1006",
        "task_name": "end",
        "method_name": "end",
        "task_type": "end",
        "method_kwargs": {},
        "prev_id": "1001",
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]
process_info = {
    'process_id': '1006',
    'process_name': 'test_parallel_with_process',
    "creator": "blue",
    "updater": None,
}

if __name__ == '__main__':
    OrderLines(process_info, nodes).start()

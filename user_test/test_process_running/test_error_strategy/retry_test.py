# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : retry_test.py
# Time       ：2023/3/11 16:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务失败重试
"""
from orderlines.app import OrderLines

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
            "a": 'test',
            "b": 2
        },
        "prev_id": "1001",
        "next_id": "1003",
        "task_config": {
            "task_strategy": 'retry'
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
    'process_id': '1002',
    'process_name': 'test_retry',
    "creator": "blue",
    "updater": None,
}

if __name__ == '__main__':
    orderlines = OrderLines()
    orderlines.clear_db()
    orderlines.start(process_info=process_info, task_nodes=data, dry=False)

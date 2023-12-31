# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : call_back_test.py
# Time       ：2023/3/11 17:19
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务运行失败后的消息通知
"""
from orderlines.app import OrderLines


def callback_task_test():
    data = [
        {
            "task_id": "1001",
            "task_name": "开始节点",
            "method_name": "start",
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
            "task_name": "加法",
            "method_name": "test_add",
            "task_type": "common",
            "method_kwargs": {
                "a": "q1",
                "b": 2
            },
            "prev_id": "1001",
            "next_id": "1003",
            "task_config": {
                "task_strategy": "raise"
            },
            "task_module": "Test",
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
            "prev_id": "1002",
            "next_id": "1004",
            "task_config": None,
            "task_module": "Test",
            "module_version": "1.0.0.1",
            "desc": None
        },
        {
            "task_id": "1004",
            "task_name": "结束节点",
            "method_name": "end",
            "task_type": "end",
            "method_kwargs": None,
            "prev_id": "1003",
            "next_id": None,
            "task_config": None,
            "task_module": "BuiltIn",
            "module_version": "1.0.0.1",
            "desc": None
        }
    ]
    process_info = {
        "process_id": "1011",
        "process_name": "test_call_back",
        "creator": "blue",
        "updater": None,
    }

    orderlines = OrderLines()
    orderlines.start(process_info=process_info, task_nodes=data, dry=False, clear_db=True)


if __name__ == '__main__':
    callback_task_test()

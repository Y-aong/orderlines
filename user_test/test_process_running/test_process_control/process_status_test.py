# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_process_status.pb
# Time       ：2023/1/27 21:48
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试流程控制——根据流程状态
"""
from orderlines.app import OrderLines

nodes = [
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
        "desc": None
    },
    {
        "task_id": "1012",
        "task_name": "add",
        "method_name": "test_add",
        "task_type": "common",
        "method_kwargs": {
            "a": 2,
            "b": 334
        },
        "prev_id": "1011",
        "next_id": "1013",
        "task_config": {
            "task_strategy": "skip"  # 需要根据运行状态进行判断的task_strategy必须为skip，不跳过直接抛错了后面怎么根据状态判断
        },
        "task_module": "Test",
        "desc": None
    },

    {
        "task_id": "1013",
        "task_name": "process_control",
        "method_name": "process_control",
        "task_type": "process_control",
        "method_kwargs": {
            "conditions": "1012",  # 这里传递task_id
            "expression": {
                "success": {"task_id": "1014"},
                "failure": {"task_id": "1015"}
            }
        },
        "prev_id": "1012",
        "next_id": None,
        "task_config": None,
        "task_module": "ProcessControl",
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
        "desc": None
    },
    {
        "task_id": "1016",
        "task_name": "end",
        "method_name": "end",
        "task_type": "end",
        "method_kwargs": None,
        "prev_id": None,
        "next_id": None,
        "task_config": None,
        "task_module": "BuiltIn",
        "desc": None
    }
]

process_info = {
    "process_id": "1008",
    "process_name": "test_process_status",
    "creator": "blue",
}

if __name__ == '__main__':
    orderlines = OrderLines()
    orderlines.clear_db()
    orderlines.start(process_info=process_info, task_nodes=nodes)

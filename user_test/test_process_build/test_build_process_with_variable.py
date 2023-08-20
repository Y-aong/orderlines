# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_build_process_with_variable.py
# Time       ：2023/8/13 9:11
# Author     ：Y-aong
# version    ：python 3.7
# Description：带有变量创建流程
"""
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter


def test_build_process_with_variable():
    task_nodes = [
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
        "process_id": "1001",
        "process_name": "test_common",
        "creator": "blue",
        "updater": None,
    }
    variable = [
        {
            "variable_key": "subtraction_value",
            "variable_value": "${return_value}",
            "variable_type": "int",
            "variable_desc": "subtraction函数的返回值"
        }
    ]
    process_build = ProcessBuildAdapter()
    process_id = process_build.build_by_dict(process_info, task_nodes, variable, clear_db=True)
    assert process_id

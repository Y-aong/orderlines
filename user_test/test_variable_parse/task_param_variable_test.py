# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_param_variable_test.py
# Time       ：2023/8/12 21:15
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试任务参数解析
"""
from orderlines.variable.common_task_strategy import CommonTaskVariableStrategy


def task_param_variable_parse():
    process_instance_id = '477febc639a311ee836a001a7dda7111'
    task_kwargs = {
        "a": "${add_result}-1",
        "b": 123
    }

    task_variable = CommonTaskVariableStrategy(process_instance_id, )
    task_result = task_variable.handle_task_kwargs(task_kwargs)
    print(task_result)


task_param_variable_parse()

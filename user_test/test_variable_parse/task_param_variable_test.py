# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : task_param_variable_test.py
# Time       ：2023/8/12 21:15
# Author     ：Y-aong
# version    ：python 3.7
# Description：测试任务参数解析
"""
from orderlines.variable.variable_handler import CommonTaskVariableStrategy


def test_task_param_variable_parse():
    # 需要替换process_instance_id
    process_instance_id = '477febc639a311ee836a001a7dda7111'
    task_kwargs = {
        "a": "${add_result}-1",
        "b": 123
    }

    task_variable = CommonTaskVariableStrategy(process_instance_id, )
    task_result = task_variable.handle_task_kwargs(task_kwargs)
    assert task_result.get('status') == 'SUCCESS'


if __name__ == '__main__':
    test_task_param_variable_parse()

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : language_type.py
# Time       ：2023/7/22 10:40
# Author     ：Y-aong
# version    ：python 3.7
# Description：语言类型
"""
from conf.config import LanguageConfig


class ZH:
    process_name = '流程名称'
    node_info = '节点信息'
    error_info = '异常信息'
    status = '任务状态'
    group_ids = '任务id'
    parallel_task_ids = '并行任务id组'
    # process_control
    conditions = '条件'
    expression = '条件表达式'
    task_id = '任务id'
    result = '任务结果'


class EN:
    process_name = 'process_name'
    node_info = 'process_node_info'
    error_info = 'process_error_info'
    status = 'process_status'
    group_ids = 'group_ids'
    parallel_task_ids = 'Parallel task id group'
    # process_control
    condition = 'judgement conditions'
    expression = 'condition expression'
    task_id = 'task_id'
    result = 'task_result'


languages = {
    'zh': ZH,
    'en': EN
}


def get_desc_with_language(attr):
    language_module = languages.get(LanguageConfig.language_type.lower())
    if not language_module:
        return ''
    if hasattr(language_module, attr):
        return getattr(language_module, attr)
    else:
        return ''

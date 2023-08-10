# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : language_type.py
# Time       ：2023/7/22 10:40
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    语言类型
    linguistic type
"""
from conf.config import LanguageConfig


class ZH:
    process_id = '流程id'
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
    task_config = '任务配置'
    process_info = '流程信息'
    process_instance_id = '流程实例id'
    task_nodes = '流程节点信息'


class EN:
    process_id = 'process id'
    process_name = 'process name'
    node_info = 'process node info'
    error_info = 'process_error info'
    status = 'process status'
    group_ids = 'group ids'
    parallel_task_ids = 'Parallel task id group'
    # process_control
    condition = 'judgement conditions'
    expression = 'condition expression'
    task_id = 'task id'
    result = 'task result'
    task_config = 'task config'
    process_info = 'process info'
    task_nodes = 'process nodes info'
    process_instance_id = 'process instance id'


languages = {
    'zh': ZH,
    'en': EN
}


def get_desc_by_lang(attr: str) -> str:
    language_module = languages.get(LanguageConfig.language_type.lower())
    if not language_module:
        return attr
    if hasattr(language_module, attr):
        return getattr(language_module, attr)
    else:
        return attr

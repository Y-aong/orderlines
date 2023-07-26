# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_orderlines_type.py
# Time       ：2023/7/22 11:07
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines 基础类型
    orderlines base type
"""
from typing import Union, List

from pydantic import BaseModel, Field

from order_lines.utils.language_type import get_desc_with_language


class BasePluginParam(BaseModel):
    process_id: str = Field(description=get_desc_with_language('process_id'), title='process_id')
    task_id: str = Field(description=get_desc_with_language('task_id'), title='task id')
    result: Union[None, list, dict] = Field(description=get_desc_with_language('result'), title='result')
    task_config: Union[None, dict] = Field(
        default=dict(), description=get_desc_with_language('task_config'), title='task config')


class GateWayParam(BasePluginParam):
    process_name: str = Field(description=get_desc_with_language('process_name'), title='process name')
    process_info: dict = Field(description=get_desc_with_language('process_info'), title='process info')
    process_node: list = Field(description=get_desc_with_language('process_node'), title='process node')


class EmailParam(BaseModel):
    process_name: str = Field(description=get_desc_with_language('precess_name'), title='precess_name')
    node_info: dict = Field(description=get_desc_with_language('node_info'), title='node_info')
    error_info: dict = Field(description=get_desc_with_language('error_info'), title='error_info')
    status: Union[str, None] = Field(description=get_desc_with_language('status'), title='status')


class EmailResult(BaseModel):
    status: str = Field(description=get_desc_with_language('status'), title='task status')


class GroupParam(GateWayParam):
    group_ids: List[str] = Field(description=get_desc_with_language('group_ids'), title='group_ids')


class ParallelParam(GateWayParam):
    parallel_task_ids: List[str] = Field(get_desc_with_language('parallel_task_ids'), title='parallel_task_ids')


class ProcessControlParam(BasePluginParam):
    conditions: list = Field(description=get_desc_with_language('conditions'), title='conditions')
    expression: dict = Field(description=get_desc_with_language('expression'), title='expression')
    process_info: dict = Field(description=get_desc_with_language('process_info'), title='process_info')


class ProcessControlResult(BaseModel):
    task_id: str = Field(description=get_desc_with_language('task_id'), title='task_id')

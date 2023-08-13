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
from typing import Union, List, Dict, Any

from pydantic import BaseModel, Field

from orderlines.utils.language_type import get_desc_by_lang


class BaseTaskConfig(BaseModel):
    task_strategy: Union[str, None] = Field(default='raise', description=get_desc_by_lang('task_strategy'))
    timeout: Union[int, None] = Field(default=120, description=get_desc_by_lang('task_timeout'))


class BaseNode(BaseModel):
    task_id: str = Field(description=get_desc_by_lang('task_id'))
    task_name: str = Field(description=get_desc_by_lang('task_name'))
    method_name: str = Field(description=get_desc_by_lang('method_name'))
    task_type: str = Field(description=get_desc_by_lang('task_type'))
    method_kwargs: Union[str, None] = Field(description=get_desc_by_lang('method_kwargs'))
    prev_id: Union[str, None] = Field(description=get_desc_by_lang('prev_id'))
    next_id: Union[str, None] = Field(description=get_desc_by_lang('next_id'))
    task_config: Union[BaseTaskConfig, None] = Field(description=get_desc_by_lang('task_config'))
    task_module: str = Field(description=get_desc_by_lang('task_module'))
    desc: Union[str, None] = Field(description=get_desc_by_lang('desc'))
    version: Union[str, None] = Field(description=get_desc_by_lang('version'))


class BaseProcessConfig(BaseModel):
    timeout: Union[int] = Field(default=2 * 60 * 60, description=get_desc_by_lang('process_timeout'))


class BaseProcessInfo(BaseModel):
    process_id: str = Field(description=get_desc_by_lang('process_id'))
    process_instance_id: str = Field(description=get_desc_by_lang('process_instance_id'))
    process_name: str = Field(description=get_desc_by_lang('process_name'))
    creator: Union[str, None] = Field(description=get_desc_by_lang('creator'))
    updater: Union[str, None] = Field(description=get_desc_by_lang('updater'))
    process_config: Union[BaseProcessConfig, None] = Field(description=get_desc_by_lang('process_config'))
    desc: Union[str, None] = Field(description=get_desc_by_lang('process_desc'))


class BaseProcessNode(BaseModel):
    process_info: BaseProcessInfo = Field(description=get_desc_by_lang('process_info'))
    task_nodes: List[BaseNode] = Field(description=get_desc_by_lang('task_nodes'))


class BasePluginParam(BaseModel):
    task_config: Union[None, dict] = Field(
        default=dict(), description=get_desc_by_lang('task_config'))


class GateWayParam(BasePluginParam):
    process_info: BaseProcessInfo = Field(description=get_desc_by_lang('process_info'))
    task_nodes: list = Field(description=get_desc_by_lang('task_nodes'))
    task_id: Union[str, None] = Field(description=get_desc_by_lang('task_id'), title='task id')


class EmailParam(BaseModel):
    process_name: str = Field(description=get_desc_by_lang('precess_name'))
    node_info: dict = Field(description=get_desc_by_lang('node_info'))
    error_info: dict = Field(description=get_desc_by_lang('error_info'))
    status: Union[str, None] = Field(description=get_desc_by_lang('status'))


class EmailResult(BaseModel):
    status: str = Field(description=get_desc_by_lang('status'))


class GroupParam(GateWayParam):
    group_ids: List[str] = Field(description=get_desc_by_lang('group_ids'))


class ParallelParam(GateWayParam):
    parallel_task_ids: List[str] = Field(description=get_desc_by_lang('parallel_task_ids'))


class BaseConditionItem(BaseModel):
    """
    流程控制以返回值控制的条件
    Process control to return value control conditions
    """
    condition: Any = Field(description=get_desc_by_lang('condition'))
    target: Any = Field(description=get_desc_by_lang('target'))
    sign: str = Field(description=get_desc_by_lang('sign'))


class BaseConditionList(BaseModel):
    condition_list: List[BaseConditionItem] = Field(description=get_desc_by_lang('condition_list'))


class BaseConditionsWithReturn(BaseModel):
    conditions: List[Dict[str, BaseConditionList]] = Field(description=get_desc_by_lang('conditions_with_return'))


class BaseExpression(BaseModel):
    expression: Dict[str, dict] = Field(description=get_desc_by_lang('expression'))


class ProcessControlParam(BasePluginParam):
    """
    with return
    "conditions": [
                {
                    'A': [{'condition': 1, 'target': "${add_value}", 'sign': '='},
                          {'condition': 1, 'target': 3, 'sign': '>'}]
                },
                {
                    'B': [{'condition': 2, 'target': "${add_value}", 'sign': '<'},
                          {'condition': 3, 'target': 3, 'sign': '='}]
                }
            ],
    "expression": {
        'A': {'task_id': "1014"},
        'B': {'task_id': "1015"}
    }
    with status
    "conditions": "1012",  # 这里传递task_id
    "expression": {
        "success": {"task_id": "1014"},
        "failure": {"task_id": "1015"}
    }
    """
    conditions: Union[list, str] = Field(description=get_desc_by_lang('conditions'))
    expression: dict = Field(description=get_desc_by_lang('expression'))
    process_info: dict = Field(description=get_desc_by_lang('process_info'))


class ProcessControlResult(BaseModel):
    task_id: str = Field(description=get_desc_by_lang('task_id'))


class TaskResultConfigType(BaseModel):
    """
    {
        "variable_name": "add_value",
        "variable_value": "${add_value}+1",
        "variable_type": "int",
        "variable_desc": "add函数的返回值"
    }
    """
    variable_key: str = Field(default=None, description=get_desc_by_lang('variable_name'))
    variable_value: str = Field(default=None, description=get_desc_by_lang('variable_value'))
    variable_type: str = Field(default=None, description=get_desc_by_lang('variable_type'))
    variable_desc: str = Field(default=None, description=get_desc_by_lang('variable_desc'))

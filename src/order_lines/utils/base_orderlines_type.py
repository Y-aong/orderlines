# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_orderlines_type.py
# Time       ：2023/7/22 11:07
# Author     ：Y-aong
# version    ：python 3.7
# Description：orderlines的基础类型
"""
from typing import Union

from pydantic import BaseModel, Field

from public.language_type import get_desc_with_language


class BasePluginResult(BaseModel):
    status: str = Field(description=get_desc_with_language('status'))


class BasePluginParam(BaseModel):
    process_id: str = Field(description='任务id')
    task_id: str = Field(description='任务id')
    result: Union[None, str, list, dict, int] = Field(description=get_desc_with_language('result'), title='result')
    __task_config__: dict = Field(default=dict(), description='任务配置')


class GateWayParam(BasePluginParam):
    process_name: str = Field(description='流程名称')
    process_info: dict = Field(description='流程信息')
    process_node: list = Field(description='流程节点')


class GroupResultType(BaseModel):
    pass

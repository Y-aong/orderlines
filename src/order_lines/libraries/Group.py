# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Group.py
# Time       ：2023/2/26 21:33
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务组
任务组
1、任务组中只可以运行普通任务，不可以运行流程控制，并发任务等任务
2、任务组是一个多个任务的集合，在主流程中只相当于一个普通节点
3、任务组是一个责任链模式，必须是确定的任务，任务组的中的子任务和其他方式的运行方式不一样
4、并发节点中只可以运行任务组就算是一个节点也要是一个任务组
5、任务组的group_ids是一个列表，包含着当前任务中的所有子任务
{
        "task_id": 1012,
        "task_name": "add",
        "method_name": "test_add",
        "task_type": "group",
        "method_kwargs": {
            "a": 2,
            "b": '786'
        },
        "prev_id": 1011,
        "group_ids": [1014, 1015],
        "next_id": 1016,
        "task_config": {
            "task_strategy": 'raise'
        },
        "task_module": "Group",
        "desc": None
    }
"""
import traceback
from typing import List

from pydantic import Field

from conf.config import OrderLinesConfig
from order_lines.libraries.BaseTask import BaseTask
from order_lines.running.listen_running import ListenRunning
from order_lines.utils.base_orderlines_type import GateWayParam, BasePluginResult

from order_lines.utils.exceptions import OrderLineStopException
from order_lines.utils.process_action_enum import StatusEnum as Status
from public.language_type import get_desc_with_language
from public.logger import logger
from order_lines.utils.utils import get_current_node


class GroupType(GateWayParam):
    group_ids: List[str] = Field(description=get_desc_with_language('group_ids'), title='group_ids')


class Group(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self, process_info, process_node: List[dict]):
        super(Group, self).__init__()
        # group node节点的task_id
        self.process_node = process_node
        self.listen_running = ListenRunning(process_info)

    def task_group(self, group_type: GroupType) -> BasePluginResult:
        """
        根据子任务id组合为任务链
        :return:
        """
        group_result = dict()
        from order_lines.handlers.task_handlers import CommonHandler
        for task_id in group_type.group_ids:
            node = get_current_node(task_id, self.process_node)
            task_type = node.get('task_type')
            assert task_type == 'common', '任务组中的子任务必须是普通任务类型'
            if node.get('task_id') == task_id:
                _handler = CommonHandler()
                task_module = node.get('task_module')
                method_name = node.get('method_name')
                task_kwargs = node.get('method_kwargs')
                task_instance, task_table_id = self.listen_running.insert(node)

                try:
                    from order_lines.running.task_build import sync_task
                    task_result = sync_task(_handler, task_module, method_name, task_kwargs)
                    logger.info(f'任务组函数运行结果:{task_result}')
                    task_status = task_result.get('status')
                    self.listen_running.update(node, task_instance, task_table_id, task_result, task_status)
                    group_result[str(task_id)] = task_result
                except OrderLineStopException as e:
                    logger.error(f'任务组函数停止:{traceback.format_exc(), e}')
                    error_info = traceback.format_exc()
                    self.listen_running.update(node, task_instance, task_table_id, error_info, Status.yellow.value)
                except Exception as e:
                    logger.error(f'任务组函数运行失败:{traceback.format_exc(), e, traceback.format_exc()}')
                    error_info = traceback.format_exc()
                    self.listen_running.update(node, task_instance, task_table_id, error_info, Status.red.value)
        return {'status': Status.green.value, **group_result}

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : trigger.py
# Time       ：2023/2/19 19:36
# Author     ：blue_moon
# version    ：python 3.7
# Description：解析流程的方式
1、使用flask线程隔离的方式进行隔离线程
2、使用队列的方式运行任务的取出和放入，这里主要考虑到多线程下的数据安全
"""
import asyncio
import datetime
from queue import Queue
from typing import List

from werkzeug.local import Local

from order_lines.api.process import Process
from order_lines.libraries.ProcessControl import ProcessControl

from order_lines.utils.process_action_enum import StatusEnum, ProcessStatus


class Trigger:
    """
    解析任务将任务id放入任务队列中
    """
    local_process = Local()

    def __init__(self, process_info: dict, process_node: List[dict]):
        self.process_instance_id = process_info.get('process_instance_id')
        self.process_name = process_info.get('process_name')
        self.process_node = process_node
        self.task_deque = Queue()
        self.start_node_id = self.get_start_node_id()
        self.current_task_id = self.start_node_id
        self.process_instance = Process(process_info)
        if not hasattr(self.local_process, self.process_instance_id):
            # 将流程运行信息插入数据
            process_instance = self.process_instance.select_data(self.process_instance_id)
            if process_instance:
                process_info.setdefault('process_status', ProcessStatus.grey.value)
                self.process_instance_table_id = self.process_instance.update_db(**process_info)
            else:
                self.process_instance_table_id = self.process_instance.insert_db()
            setattr(self.local_process, self.process_instance_id, self.task_deque)
            self.task_deque.put(self.start_node_id)

    @property
    def current_time(self):
        return datetime.datetime.utcnow()

    def get_start_node_id(self) -> int:
        """
        获取流程/子流程中的开始节点
        :return: 返回流程的开始节点id，子流程开始节点
        """
        task_ids = list()
        for node in self.process_node:
            if node.get('method_name') == 'start':
                return node.get('task_id')
            else:
                task_ids.append(node.get('task_id'))
        task_ids.sort()
        return task_ids.pop()

    def get_next_node_id(self) -> int:
        """
        根据当前当前正在运行的id获取到下一个要运行node_id
        :return:
        """
        for node in self.process_node:
            if node.get('task_id') == self.current_task_id:
                if node.get('task_type') == 'process_control':
                    # next_id等于流程控制函数运行后的返回值
                    process_control_kw: dict = node.get('method_kwargs')
                    return ProcessControl().process_control(**process_control_kw)
                return node.get('next_id')
        return 0

    async def update_process_info(self, process_status: str, error_info=None):
        """
        修改流程状态
        :param process_status: 流程状态
        :param error_info: 流程错误信息
        :return:
        """
        process_info = {
            'end_time': self.current_time,
            'process_status': process_status,
            'process_error': error_info
        }
        self.process_instance.update_db(self.process_instance_id, **process_info)

    async def parse(self):
        """
        将流程id放入队列中
        :return:
        """
        _next_node_id = self.get_next_node_id()
        if not _next_node_id:
            await self.update_process_info(StatusEnum.green.value)
            return False

        if self.task_deque.empty():
            # 当队列为空代表着这个任务已经运行成功
            self.task_deque.put(_next_node_id)
            self.current_task_id = _next_node_id
            await asyncio.sleep(0.01)
            return True
        else:
            return False

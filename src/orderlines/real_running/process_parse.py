# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : process_parse.py
# Time       ：2023/8/1 10:26
# Author     ：YangYong
# version    ：python 3.10
# Description：
解析流程

1、使用flask线程隔离的方式进行隔离线程
2、使用队列的方式运行任务的取出和放入，这里主要考虑到多线程下的数据安全

Parser process

1. Use flask thread isolation to isolate threads
2, the use of queues to run the extraction and insertion of tasks, mainly considering the data security
 under multi-threading
"""
from abc import abstractmethod

from werkzeug.local import LocalStack


from orderlines.real_running.app_context import AppContext
from orderlines.real_running.base_runner import BaseRunner
from orderlines.real_running.running_db_operator import RunningDBOperator
from orderlines.utils.base_orderlines_type import ProcessControlParam
from orderlines.utils.exceptions import OrderlinesHasNoStart
from orderlines.utils.process_action_enum import ProcessStatus


class BaseParse(BaseRunner):
    def __init__(self, process_instance_id: str, context: AppContext):
        super(BaseParse, self).__init__(process_instance_id, context)
        # 初始化，开始当前执行id为start node id
        self.current_task_id = self.start_node_id()
        process_id = self.context.get_process_item(self.process_instance_id, 'process_id')
        self.running_db_operator = RunningDBOperator(process_instance_id, process_id)

    def get_next_node_id(self) -> str:
        """
        获取下一个要运行的任务
        get next will run task
        @return:
        """
        for node in self.task_nodes:
            if node.get('task_id') == self.current_task_id:
                if node.get('task_type') == 'process_control':
                    process_control_kw: dict = node.get('method_kwargs')
                    process_control_param = ProcessControlParam(**process_control_kw)
                    from orderlines.libraries.ProcessControl import ProcessControl
                    return ProcessControl().process_control(process_control_param)
                return node.get('next_id')
        return None

    def start_node_id(self) -> str:
        """
        获取流程开始节点
        Gets the start node in the process
        @return:
            返回流程的开始节点id
            Returns the id of the start node of the process
        """
        for node in self.task_nodes:
            if node.get('method_name') == 'start':
                return node.get('task_id')
        raise OrderlinesHasNoStart('orderlines process has no start node')

    @abstractmethod
    def parse(self) -> bool:
        pass


class ProcessParse(BaseParse):
    def __init__(self, process_instance_id: str, context: AppContext):
        super(ProcessParse, self).__init__(process_instance_id, context)
        self.stock = LocalStack()
        self.stock.push(self.current_task_id)

    def parse(self) -> bool:
        """
        采用LocalStack进行存放数据
        @return:
        """
        _next_task_id = self.get_next_node_id()
        if not _next_task_id:
            # set process instance success, this is process is complete
            self.running_db_operator.process_instance_update(ProcessStatus.green.value)
            return False
        else:
            # When the stock is empty, the task has run successfully
            self.stock.push(_next_task_id)
            self.current_task_id = _next_task_id
            return True

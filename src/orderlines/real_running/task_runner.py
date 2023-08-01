# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : task_runner.py
# Time       ：2023/8/1 10:26
# Author     ：YangYong
# version    ：python 3.10
# Description：
    流程运行
    process running
"""
import asyncio
import threading

import async_timeout

from orderlines.real_running.app_context import AppContext
from orderlines.real_running.process_parse import ProcessParse
from orderlines.real_running.task_build import TaskBuild


class TaskRunner(threading.Thread):

    def __init__(self, process_instance_id: str, context: AppContext, dry):
        super(TaskRunner, self).__init__()
        self.process_instance_id = process_instance_id
        self.context = context
        self.dry = dry
        self.parse = ProcessParse(process_instance_id, context)
        self.task_build = TaskBuild(process_instance_id, context)
        self.task_stock = self.parse.stock
        self.running_db_operator = self.parse.running_db_operator
        self.stop = False
        self.is_run = True
        self.current_task_id = self.task_stock.top

    @property
    def current_node(self):
        return self.context.get_task_node(self.process_instance_id, self.current_task_id)

    def run(self) -> None:
        pass

    def task_run(self):
        while self.is_run and not self.stop:
            task_instance_id = self.running_db_operator.task_instance_insert(self.current_node, self.dry)

    def on_running(self, task_instance_id: str):
        """
        任务运行时
        Task runtime
        @param task_instance_id: 任务实例id
        @return:
        """
        task_config = self.context.get_task_node_item(self.process_instance_id, self.current_task_id, 'task_config')
        task_timeout = task_config.get('timeout')
        async with async_timeout.timeout(task_timeout):
            task = asyncio.create_task(self.task_build.build(self.current_task_id))
            await task
            task_result: dict = task.result()

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : enter_point.py
# Time       ：2023/3/7 21:04
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines 入口
    orderlines enter point
"""
import threading
import time
import uuid
from typing import List

from order_lines.operators.process import ProcessInstanceOperator
from order_lines.running.listen_running import ListenRunning
from order_lines.running.runner import TaskRunner
from public.base_model import get_session

from public.logger import logger
from order_lines.utils.process_action_enum import StatusEnum


class OrderLines:
    def __init__(self, process_info: dict, process_node: List[dict]):
        self.process_info = process_info
        self.process_node = process_node
        self.process_instance_id = str(uuid.uuid1().hex)
        self.process_name = process_info.get('process_name')
        self.process_info['process_instance_id'] = self.process_instance_id
        self.session = get_session()
        self.listen_running = ListenRunning(self.process_info)

    def watch_dog(self):
        """
        任务运行看门狗。每隔0.5秒检查一下数据库，查看流程运行实例的process_status
        Task run watchdog.Check the database every 0.5 seconds to see the process_status of the process running instance
        :return:
        """
        process_instance = ProcessInstanceOperator.select_data(self.process_instance_id)
        process_status = process_instance.process_status if process_instance else None
        if process_status == StatusEnum.yellow.value:
            task_names = self.listen_running.stop_helper(self.process_instance_id)
            logger.info(f'task {",".join(task_names)} stop')

        while process_status in [StatusEnum.grey.value, StatusEnum.blue.value]:
            process_instance = ProcessInstanceOperator.select_data(self.process_instance_id)
            process_status = process_instance.process_status
            if process_status == StatusEnum.green.value:
                logger.info(f'process {self.process_name} run success')
                break
            elif process_status == StatusEnum.red.value:
                logger.info(f'process {self.process_name} run failure')
                break
            elif process_status == StatusEnum.yellow.value:
                task_names = self.listen_running.stop_helper(self.process_instance_id)
                logger.info(f'task {",".join(task_names)} stop, {self.process_instance_id}')
                break

            time.sleep(0.5)

    def run(self):
        t = TaskRunner(self.process_info, self.process_node, self.listen_running)
        t.start()

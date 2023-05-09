# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : OrderLines.py
# Time       ：2023/3/7 21:04
# Author     ：blue_moon
# version    ：python 3.7
# Description：order_lines入口
"""
import asyncio
import datetime
import threading
import uuid
from typing import List

from conf.config import OrderLinesConfig
from flask_app.public.base_model import get_session
from order_lines.api.process import Process
from order_lines.running.listen_running import ListenRunning
from order_lines.running.runner import TaskRunner
from order_lines.utils.exceptions import TimeOutException

from order_lines.utils.logger import logger
from order_lines.utils.process_action_enum import StatusEnum


class OrderLines:
    def __init__(self, process_info: dict, process_node: List[dict]):
        self.process_info = process_info
        self.process_node = process_node
        self.process_instance_id = str(uuid.uuid1())
        self.process_name = process_info.get('process_name')
        self.process_info['process_instance_id'] = self.process_instance_id
        self.session = get_session()
        self.listen_running = ListenRunning(self.process_info)

    def process_is_timeout(self) -> bool:
        """
        获取流程的运行时长
        :return:
        """
        current_time = datetime.datetime.now()
        process = Process(self.process_info)
        process_instance = process.select_data(self.process_instance_id)
        start_time = process_instance.start_time
        process_config = self.process_info.get('process_config')
        timeout = process_config.get('timeout') if process_config else OrderLinesConfig.process_timeout
        time_interval = (current_time - start_time).seconds
        flag = time_interval > timeout and current_time > start_time

        if flag:
            update_data = {
                'process_error_info': f'流程{self.process_name}运行超时',
                'process_status': StatusEnum.red.value
            }
            logger.info(f'流程超时运行时间:{time_interval},{flag}, {start_time}, {current_time}')
            process.update_db(self.process_instance_id, **update_data)
        return flag

    async def watch_dog(self):
        """
        任务运行看门狗，
        每隔0.1秒检查一下数据库，查看流程运行实例的task_status,如果是停止的就抛出OrderLineStopException停止流程
        :return:
        """
        process_instance = Process.select_data(self.process_instance_id)
        process_status = process_instance.process_status if process_instance else None
        if process_status == StatusEnum.yellow.value:
            task_names = self.listen_running.stop_helper(self.process_instance_id)
            logger.info(f'任务{",".join(task_names)}停止')

        while process_status in [StatusEnum.grey.value, StatusEnum.blue.value]:
            process_instance = Process.select_data(self.process_instance_id)
            process_status = process_instance.process_status
            # 检查是否停止
            if process_status == StatusEnum.green.value:
                logger.info(f'流程{self.process_name}正常运行结束')
                break
            elif process_status == StatusEnum.red.value:
                logger.info(f'流程{self.process_name}运行失败')
                break
            elif process_status == StatusEnum.yellow.value:
                task_names = self.listen_running.stop_helper(self.process_instance_id)
                logger.info(f'任务{",".join(task_names)}停止, {self.process_instance_id}')

            # 检查是否超时
            if self.process_is_timeout():
                logger.info(f'流程{self.process_name}运行超时')
                raise TimeOutException(f'流程{self.process_name}运行超时')

            await asyncio.sleep(0.5)

    def run(self):
        t = TaskRunner(self.process_info, self.process_node, self.listen_running)
        # t.daemon = True
        t.start()
        # 单独启动一个线程来运行看门狗，看门狗主要是根据数据库任务状态来监控流程的运行状态
        threading.Thread(target=self.watch_dog, args=())

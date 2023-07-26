# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : runner_handler.py
# Time       ：2023/2/16 21:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程运行
    process running
"""
import asyncio
import json
import threading

import traceback
from typing import List
import async_timeout

from conf.config import OrderLinesConfig
from order_lines.running.running_strategy import RunningStrategy
from order_lines.running.task_build import build_task
from order_lines.utils.exceptions import OrderLineStopException
from public.logger import logger
from order_lines.utils.process_action_enum import StatusEnum
from order_lines.running.trigger import Trigger
from order_lines.utils.utils import get_current_node


class TaskRunner(threading.Thread):
    stop = False

    def __init__(self, process_info: dict, process_node: List[dict], listen_running):
        super(TaskRunner, self).__init__()
        self.process_info = process_info
        self.process_instance_id = process_info.get('process_instance_id')
        self.process_node = process_node
        self.trigger = Trigger(process_info, process_node)
        self.task_deque = self.trigger.task_deque
        self.listen_running = listen_running
        self.current_task_id = None
        self.is_run = True
        self.variable_handler = None

    def run(self) -> None:
        asyncio.run(self.task_run())

    def get_task_timeout(self):
        task_config = get_current_node(self.current_task_id, self.process_node).get('task_config')
        if task_config and isinstance(task_config, str):
            task_config = json.loads(task_config)
        elif task_config and isinstance(task_config, dict):
            task_config = task_config
        else:
            task_config = dict()
        return task_config.get('timeout') if task_config.get('timeout') else OrderLinesConfig.task_timeout

    async def process_is_stop(self):
        process_instance = self.trigger.process_instance.select_data(self.process_instance_id)
        process_status = process_instance.process_status
        if process_status == StatusEnum.yellow.value:
            return True
        return False

    async def task_run(self):
        """Actually run the task node"""
        while self.is_run and not self.stop:
            # get node
            self.current_task_id = self.task_deque.get()
            current_node = get_current_node(self.current_task_id, self.process_node)
            task_instance, task_table_id = self.listen_running.insert(current_node)
            await self.trigger.update_process_info(StatusEnum.blue.value)
            try:
                await asyncio.gather(self.on_running(current_node, task_instance, task_table_id))
            except OrderLineStopException as e:
                await self.on_stop(e, current_node, task_instance, task_table_id)
            except Exception as e:
                await self.on_failure(e, current_node, task_instance, task_table_id)

            self.stop = await self.process_is_stop()
            if not self.is_run and not self.stop:
                logger.info(
                    f'process name:{self.process_info.get("process_name")},'
                    f'process id:{self.process_info.get("process_id")} run complete')
                break
            await asyncio.sleep(0.01)

    async def on_running(self, current_node, task_instance, task_table_id):
        """Processing at run time"""
        timeout = self.get_task_timeout()
        async with async_timeout.timeout(timeout):
            task = asyncio.create_task(build_task(self.process_node, self.current_task_id, self.process_info))
            await task
            task_result: dict = task.result()
            strategy = RunningStrategy(
                self.process_info, self.process_node, self.current_task_id, self.trigger, timeout)
            self.is_run, task_or_error, task_status = await strategy.running_strategy(task_result, current_node)
            self.listen_running.update(current_node, task_instance, task_table_id, task_or_error, task_status)
            if task_status != StatusEnum.green.value:
                await self.trigger.update_process_info(StatusEnum.red.value, traceback.format_exc())

    async def on_stop(self, err, current_node, task_instance, task_table_id):
        """The operation when the task stops"""
        error_info = traceback.format_exc()
        logger.info(f'current_task_id::{self.current_task_id}, run stop::{error_info, err}')
        self.listen_running.update(current_node, task_instance, task_table_id, error_info, StatusEnum.yellow.value)
        await self.trigger.update_process_info(StatusEnum.yellow.value, traceback.format_exc())
        self.is_run = False

    async def on_failure(self, err, current_node, task_instance, task_table_id):
        """The operation when the task fails"""
        if isinstance(err, asyncio.TimeoutError):
            error_info = {'error_info': 'The task has timeout. Check timeout'}
            logger.info(f'current_task_id::{self.current_task_id}, run timeout::{error_info, err}')
        else:
            error_info = {'error_info': traceback.format_exc()}
            logger.info(f'current_task_id::{self.current_task_id}, run timeout::{error_info, err}')
        timeout = self.get_task_timeout()
        strategy = RunningStrategy(self.process_info, self.process_node, self.current_task_id, self.trigger, timeout)
        self.is_run, task_or_error, task_status = await strategy.running_strategy(error_info, current_node)

        self.listen_running.update(current_node, task_instance, task_table_id, error_info, task_status)
        if task_status == StatusEnum.red.value:
            await self.trigger.update_process_info(task_status, traceback.format_exc())

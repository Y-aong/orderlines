# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : running_strategy.py
# Time       ：2023/8/1 10:26
# Author     ：YangYong
# version    ：python 3.10
# Description：
    任务运行策略
    task run strategy when task run error
"""
import asyncio

import async_timeout

from orderlines.real_running.app_context import AppContext
from orderlines.real_running.base_runner import BaseRunner
from orderlines.real_running.process_parse import ProcessParse
from orderlines.real_running.task_build import TaskBuild
from orderlines.utils.exceptions import OrderLineRunningException
from orderlines.utils.orderlines_enum import TaskStatus


class RunningStrategy(BaseRunner):
    def __init__(
            self,
            process_instance_id: str,
            context: AppContext,
            current_task_id: str,
            process_parse: ProcessParse,
            error_info: dict,
            task_build: TaskBuild
    ):
        super(RunningStrategy, self).__init__(process_instance_id, context)
        self.current_task_id = current_task_id
        self.process_parse = process_parse
        self.error_info = error_info
        self.task_build = task_build
        self._task_config = self.task_config(self.current_task_id)
        self.task_timeout = self._task_config.get('timeout')
        self.strategy_context = {
            'RAISE': self.raise_strategy,
            'SKIP': self.skip_strategy,
            'RETRY': self.retry_strategy
        }

    async def skip_strategy(self):
        flag = self.process_parse.parse()
        return flag, self.error_info, TaskStatus.green.value

    async def raise_strategy(self):
        return False, self.error_info, TaskStatus.red.value

    async def retry_strategy(self):
        retry_time = self._task_config.get('retry_time')
        time = 1
        while time < retry_time:
            try:
                self.logger.info(f'Start retry {time} times')
                async with async_timeout.timeout(self.task_timeout):
                    task = asyncio.create_task(
                        self.task_build.build(self.current_task_id, self.process_info, self.task_nodes)
                    )
                    await task
                    task_result = task.result()
                    if task_result.get('status') == TaskStatus.green.value:
                        flag = self.process_parse.parse()
                        return flag, task_result, TaskStatus.green.value
                    else:
                        raise OrderLineRunningException(f'task retry run error {task_result.get("error_info")}')
            except Exception as error:
                _error_info = f'The number of retries exceeded the maximum:{time}. Error message::{error}'
                self.error_info['error_info'] = _error_info
                self.logger.info(_error_info)
                time += 1

        self.error_info['status'] = TaskStatus.red.value
        return False, self.error_info, TaskStatus.red.value

    async def handle_strategy(self) -> tuple:
        """
        处理异常的策略，Policy for handling exceptions
        @return:is_run:bool, error_info:dict, task_status:str
        """
        task_strategy = self._task_config.get('task_strategy').upper()
        self.logger.info(f'current task id {self.current_task_id} task_strategy is {task_strategy}')
        return await asyncio.create_task(self.strategy_context.get(task_strategy)())

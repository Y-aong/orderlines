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
import traceback
from typing import Any

import async_timeout

from orderlines.real_running.app_context import AppContext
from orderlines.real_running.process_parse import ProcessParse
from orderlines.real_running.running_check import CheckModule
from orderlines.real_running.running_strategy import RunningStrategy
from orderlines.real_running.task_build import TaskBuild
from orderlines.utils.exceptions import OrderLineRunningException, OrderLineStopException
from orderlines.utils.process_action_enum import TaskStatus, ProcessStatus
from orderlines.utils.utils import get_method_param_annotation
from public.logger import logger


class TaskRunner(threading.Thread):

    def __init__(self, process_instance_id: str, context: AppContext, dry):
        super(TaskRunner, self).__init__()
        self.process_instance_id = process_instance_id
        self.context = context
        self.dry = dry
        self.process_name = self.context.get_process_item(process_instance_id, 'process_name')
        self.process_parse = ProcessParse(process_instance_id, context)
        self.task_build = TaskBuild(process_instance_id, context)
        self.task_stock = self.process_parse.stock
        self.running_db_operator = self.process_parse.running_db_operator
        self.stop = False  # 是否停止
        self.paused = False  # 是否暂停
        self.is_run = True  # 根据状态判断
        self.logger = logger
        self.current_task_id = self.task_stock.top

    def current_node(self):
        return self.context.get_task_node(self.process_instance_id, self.current_task_id)

    def callback(self, task_status: str, result_or_error: dict) -> None:
        """
        on task run error callback func method
        @param task_status: task run status
        @param result_or_error: result or error
        @return:
        """
        task_config = self.process_parse.task_config(self.current_task_id)
        notice_type = task_config.get('notice_type')
        callback_func = task_config.get('callback_func')
        callback_module = task_config.get('callback_module')

        module_check = CheckModule()
        module_check.check_module(callback_module)
        callback_class = module_check.modules.get(callback_module)
        if task_status in notice_type:
            method = getattr(callback_class(), callback_func)
            flag, annotation = get_method_param_annotation(method)
            callback_param = {
                'process_name': self.process_name,
                'node_info': self.current_node(),
                'error_info': result_or_error,
                'status': task_status
            }
            self.logger.info(f'callback func is {callback_func}, callback param is {callback_param}')
            callback_func_param = annotation(**callback_param)
            method(callback_func_param)

    def run(self) -> None:
        asyncio.run(self.task_run())

    async def task_run(self) -> None:
        """
        real task run
        @return:
        """
        self.running_db_operator.process_instance_update(process_status=ProcessStatus.blue.value)

        while self.is_run and not self.stop:
            task_instance_id = self.running_db_operator.task_instance_insert(self.current_node(), self.dry)

            try:
                task_status, result_or_error = await self.on_running(task_instance_id)
            except OrderLineStopException as error:
                task_status, result_or_error = await self.on_stop(error, task_instance_id)
            except Exception as error:
                task_status, result_or_error = await self.on_failure(error, task_instance_id)
            if task_status != TaskStatus.green.value:
                self.callback(task_status, result_or_error)

            self.stop, self.paused = self.running_db_operator.process_instance_is_stop_or_paused()
            if self.stop:
                self.logger.info(f'process name {self.process_name} is stop')
                break
            if not self.is_run:
                self.logger.info(f'process name {self.process_name} run complete')
                break

            sleep_time = 10 if self.paused else 0.01

            if not self.paused:
                # if process not paused get next
                self.is_run = self.process_parse.parse()
                self.current_task_id = self.task_stock.top
            self.logger.info(f'current task id {self.current_task_id}, task result {result_or_error}\n '
                             f'is run::{self.is_run}, stop::{self.stop}, paused::{self.paused}')
            await asyncio.sleep(sleep_time)

    async def on_running(self, task_instance_id: str) -> tuple:
        """
        任务运行时
        on task runtime
        @param task_instance_id: 任务实例id
        @return:
            task_status: 任务状态
            result_or_error: 异常信息or任务结果
        """
        task_config = self.process_parse.task_config(self.current_task_id)
        task_timeout = task_config.get('timeout')
        async with async_timeout.timeout(task_timeout):
            task = asyncio.create_task(self.task_build.build(self.current_task_id))
            await task
            # maybe this is result or error, you can judge by status
            result_or_error: dict = task.result()
            status = result_or_error.get('status')
            if status != TaskStatus.green.value:
                raise OrderLineRunningException(result_or_error.get('error_info'))
            else:
                self.running_db_operator.task_instance_update(
                    task_instance_id,
                    task_status=TaskStatus.green.value,
                    result=result_or_error,
                    dry=self.dry
                )
        return result_or_error.get('status'), result_or_error

    async def on_stop(self, error: Any, task_instance_id: str):
        """
        on task stop
        @param error: error info
        @param task_instance_id: task instance id
        @return:
            task_status: 任务状态
            error_info: 异常信息
        """
        self.logger.info(f'current_task_id:{self.current_task_id} run stop.error: {traceback.format_exc()}')
        self.running_db_operator.task_instance_update(
            task_instance_id,
            task_status=TaskStatus.yellow.value,
            error_info=str(error),
            dry=self.dry
        )
        self.running_db_operator.process_instance_update(
            process_status=ProcessStatus.yellow.value,
            error_info=str(error),
            dry=self.dry
        )
        self.is_run = False

        return ProcessStatus.yellow.value, str(error)

    async def on_failure(self, error: Any, task_instance_id: str) -> tuple:
        """
        on task failure
        @param error: task error info
        @param task_instance_id: task instance id
        @return:
            task_status: 任务状态
            error_info: 异常信息
        """
        if isinstance(error, asyncio.TimeoutError):
            error_info = {'error_info': 'The task has timeout. Check timeout in task config'}
            self.logger.info(f'current_task_id::{self.current_task_id}, run timeout::{error_info}')
        else:
            error_info = {'error_info': error}
            logger.info(f'current_task_id::{self.current_task_id}, run timeout::{error_info}')

        running_strategy = RunningStrategy(
            process_instance_id=self.process_instance_id,
            context=self.context,
            current_task_id=self.current_task_id,
            process_parse=self.process_parse,
            error_info=error_info,
            task_build=self.task_build
        )
        self.is_run, result_or_error, task_status = await running_strategy.handle_strategy()

        self.running_db_operator.task_instance_update(
            task_instance_id,
            task_status=task_status,
            result=result_or_error if task_status == TaskStatus.green.value else None,
            error_info=result_or_error if task_status != TaskStatus.green.value else None,
            dry=self.dry
        )
        if task_status == TaskStatus.red.value:
            self.running_db_operator.process_instance_update(
                process_status=ProcessStatus.red.value,
                error_info=error,
                dry=self.dry
            )
        return task_status, error_info

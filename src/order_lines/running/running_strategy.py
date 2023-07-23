# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : running_strategy.py
# Time       ：2023/2/26 10:23
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务运行过程中的异常处理策略
            重试，抛出，忽略
"""
import asyncio

import async_timeout

from conf.config import OrderLinesConfig
from order_lines.running.module_check import CheckModule
from order_lines.running.task_build import build_task
from order_lines.utils.utils import get_method_param_annotation
from public.logger import logger
from order_lines.utils.process_action_enum import StatusEnum as Status


class BaseStrategy:
    def __init__(self, process_name: str, node_info: dict, ):
        self.process_name = process_name
        self.node_info = node_info

    def handle(self, notice_type: str, status: str, callback_func=None, error_or_result=None):
        """
        任务运行出错，异常的处理策略
        :param notice_type:
        :param error_or_result:
        :param status:
        :param callback_func:
        :return:
        """
        callback_func = callback_func if callback_func else OrderLinesConfig.callback_func
        module_check = CheckModule()
        module_check.check_module(OrderLinesConfig.callback_module)
        module = module_check.modules.get(OrderLinesConfig.callback_module)
        if notice_type:
            method = getattr(module(), callback_func)
            flag, annotation = get_method_param_annotation(method)
            if flag:
                email_info = {'process_name': self.process_name, 'node_info': self.node_info,
                              'error_info': error_or_result, 'status': status}
                callback_func_param = annotation(**email_info)
                method(callback_func_param)


class RunningStrategy:
    def __init__(self, process_info, process_node, current_task_id, trigger, timeout):
        self.process_info = process_info
        self.process_name = process_info.get('process_name')
        self.process_node = process_node
        self.current_task_id = current_task_id
        self.timeout = timeout
        self.trigger = trigger

    async def running_strategy(self, error_or_result, current_node: dict):
        """
        任务运行过程中的异常处理策略
        :param error_or_result:
        :param current_node:
        :return:
        """
        task_config: dict = current_node.get('task_config')
        task_config = task_config if isinstance(task_config, dict) else {}
        notice_type = task_config.get('notice_type', 'failure')
        # 任务运行状态中的异常处理策略，这里保持和流程状态一致
        task_strategy = task_config.get('task_strategy', 'raise').upper()
        callback_func = task_config.get('callback_func', OrderLinesConfig.callback_func)

        if isinstance(error_or_result, dict) and error_or_result.get('status') == Status.green.value:
            # 使用数据
            flag = await self.trigger.parse()
            return flag, error_or_result, Status.green.value
        else:
            # 调用回调函数
            strategy = BaseStrategy(self.process_name, current_node)
            status = error_or_result.get('status')
            strategy.handle(notice_type, status, callback_func, error_or_result)
        # 直接抛错
        if task_strategy == 'RAISE':
            return False, error_or_result, Status.red.value
        # 忽略错误
        elif task_strategy == Status.pink.value:
            await self.trigger.parse()
            error_or_result['status'] = Status.pink.value
            return True, error_or_result, Status.pink.value
        # 任务重试
        elif task_strategy == Status.orange.value:
            return await self.retry_strategy(error_or_result)

    async def retry_strategy(self, error_or_result):
        """重试策略"""
        retry_time = OrderLinesConfig.retry_time
        flag = 1
        while flag < retry_time:
            try:
                logger.info(f'开始重试第{flag}次')

                async with async_timeout.timeout(self.timeout):
                    task = asyncio.create_task(
                        build_task(self.process_node, self.current_task_id, self.process_info))
                    await task
                if task.result().get('status') == Status.green.value:
                    flag = await self.trigger.parse()
                    return flag, task.result(), Status.green.value
                else:
                    flag += 1
            except Exception as e:
                _error_info = f'第{flag}次报错。错误信息::{e}'
                logger.info(_error_info)
                flag += 1
        error_or_result['status'] = Status.red.value
        return False, error_or_result, Status.red.value

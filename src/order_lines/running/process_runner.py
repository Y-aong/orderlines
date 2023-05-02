# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_runner.py
# Time       ：2023/2/19 22:30
# Author     ：blue_moon
# version    ：python 3.7
# Description：使用进程方式运行任务
"""
from multiprocessing import Pool, context

from order_lines.conf.config import OrderLinesConfig
from order_lines.utils.const import CPU_COUNT
from order_lines.utils.exceptions import TimeOutException


class ProcessRunner:
    def __init__(self, pool_size: int = None, ):
        if not pool_size:
            pool_size = CPU_COUNT

        self.pool_size = pool_size

    def spawn(self, func, parallel_task_ids: list, timeout):
        """
        进程方式运行函数
        :param func:要运行的函数
        :param parallel_task_ids:并行任务函数
        :param timeout:超时时间
        :return:
        """
        try:
            pool = Pool(self.pool_size)
            task_result = dict()
            timeout = timeout if timeout else OrderLinesConfig.task_timeout
            for group_id in parallel_task_ids:
                t = pool.apply_async(func, args=(group_id,))
                task_result[group_id] = t
            for group_id, task in task_result.items():
                task_result[group_id] = task.get(timeout=timeout)

            return task_result
        except context.TimeoutError:
            raise TimeOutException(f'流程运行超时')

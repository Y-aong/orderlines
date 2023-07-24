# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_runner.py
# Time       ：2023/2/19 22:30
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    使用进程方式运行任务
    Run tasks in process mode
"""
from multiprocessing import Pool, context
from conf.config import OrderLinesConfig
from order_lines.utils.const import CPU_COUNT
from order_lines.utils.exceptions import TimeOutException
from public.logger import logger


class ProcessRunner:
    def __init__(self, pool_size: int = None, ):
        if not pool_size:
            pool_size = CPU_COUNT

        self.pool_size = pool_size

    def spawn(self, method, parallel_task_ids: list, parallel_type, timeout):
        """
        进程方式运行函数
        Run functions in process mode
        :param method:target method
        :param parallel_task_ids:parallel task ids
        :param parallel_type:parallel task param
        :param timeout:timeout
        :return:
        """
        try:
            logger.info('parallel with process')
            pool = Pool(self.pool_size)
            task_result = dict()
            timeout = timeout if timeout else OrderLinesConfig.task_timeout
            for group_id in parallel_task_ids:
                t = pool.apply_async(method, args=(group_id, parallel_type))
                task_result[group_id] = t
            for group_id, task in task_result.items():
                task_result[group_id] = task.get(timeout=timeout)

            return task_result
        except context.TimeoutError:
            raise TimeOutException(f'Process running timeout')

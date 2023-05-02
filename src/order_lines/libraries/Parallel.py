# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Parallel.py
# Time       ：2023/2/27 22:53
# Author     ：blue_moon
# version    ：python 3.7
# Description：并行网关
并行网关
1、并行网关中运行的是任务组，就算只是运行一个任务也是一个任务组
2、并行网关可以使用两种方式来运行
    2.1 协程方式这种主要的运行方式就是使用协程的方式来运行，主要针对于io密集行数据
    2.2 进程方式这种是真正的并行，主要针对的是计算密集型
3、并行网关实际上也是一个任务集合的封装，其中只可以运行普通任务
4、并行任务有两种组合方式
    第一：声明式：并行任务中声明为任务组id，即parallel_task_ids中声明为任务组的id，这是在创建时就将任务组声明了
    第二：寻找式：并行任务中为所有的任务id,让框架自己寻找任务组，但是任务中必须要有pre_id和next_id
"""
from typing import List
import gevent

from order_lines.conf.config import OrderLinesConfig
from order_lines.libraries.BaseTask import BaseTask
from order_lines.running.process_runner import ProcessRunner
from order_lines.utils.parallel_util import ParallelUtils
from order_lines.utils.utils import get_current_node


class Parallel(BaseTask):
    def __init__(self, process_info, process_node):
        super(Parallel, self).__init__()
        self.process_info = process_info
        self.process_node = process_node
        self.parallel_helper = ParallelUtils(self.process_node)

    def check_is_group(self, parallel_task_id) -> bool:
        """检查参数中是不是group_id"""
        for task_id in parallel_task_id:
            current_node = get_current_node(task_id, self.process_node)
            if current_node.get('task_type') == 'group':
                return True
        return False

    def get_group(self, parallel_task_id: list):
        """
        并行任务的第二种运行方式，是让框架自己帮你寻找任务组
        :param parallel_task_id: 任务id
        :return:
        """
        flag = self.check_is_group(parallel_task_id)
        if flag:
            return parallel_task_id
        else:
            return self.parallel_helper.get_group_id(parallel_task_id)

    def build_group_task(self, group_id):
        """
        获取的任务组
        :param group_id:并行任务id
        :return:
        """
        for node in self.process_node:
            if node.get('task_id') == group_id:
                group_ids = node.get('method_kwargs').get('group_ids')
                from order_lines.libraries.Group import Group
                group = Group(self.process_info, self.process_node)
                return group.task_group(group_ids)

    def parallel_task(self, parallel_task_ids: List[int], **kwargs):
        """
        运行并行任务组
        :param parallel_task_ids:并行任务id组
        :return:
        """
        task_config = kwargs.get('__task_config__')
        task_config = task_config if task_config else {}
        parallel_task_ids = self.get_group(parallel_task_ids)
        runner_type = task_config.get('runner')
        if runner_type == 'process':
            print(f'使用进程')
            return self.parallel_by_process(parallel_task_ids, task_config)
        else:
            return self.parallel_by_gevent(parallel_task_ids, task_config)

    def parallel_by_gevent(self, parallel_task_ids, task_config):
        """
        使用gevent协程并行
        :param parallel_task_ids:并行任务id组
        :param task_config:任务配置信息
        :return:
        """
        timeout = task_config.get('timeout')
        timeout = timeout if timeout else OrderLinesConfig.task_timeout
        jobs = [gevent.spawn(self.build_group_task, group_ids) for group_ids in parallel_task_ids]
        gevent.joinall(jobs, timeout=timeout)
        return {parallel_task_ids[index]: job.value for index, job in enumerate(jobs)}

    def parallel_by_process(self, parallel_task_ids, task_config: dict):
        """
        使用进程的方式并行，这主要适用计算密集型
        :param parallel_task_ids: 并行任务id组
        :param task_config: 任务配置信息
        :return:
        """
        pool_size = task_config.get('pool_size')
        timeout = task_config.get('timeout')
        process_runner = ProcessRunner(pool_size)
        return process_runner.spawn(self.build_group_task, parallel_task_ids, timeout)

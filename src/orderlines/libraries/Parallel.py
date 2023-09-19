# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Parallel.py
# Time       ：2023/2/27 22:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：
并行网关

1、并行网关中运行的是任务组，就算只是运行一个任务也是一个任务组
2、并行网关可以使用两种方式来运行
    2.1 协程方式这种主要的运行方式就是使用协程的方式来运行，主要针对于io密集行数据
    2.2 进程方式这种是真正的并行，主要针对的是计算密集型
3、并行网关实际上也是一个任务集合的封装，其中只可以运行普通任务
4、并行任务有两种组合方式
    第一：声明式：并行任务中声明为任务组id，即parallel_task_ids中声明为任务组的id，这是在创建时就将任务组声明了
    第二：寻找式：并行任务中为所有的任务id,让框架自己寻找任务组，但是任务中必须要有pre_id和next_id

Parallel gateway

1, parallel gateway running is a task group, even if only running a task is a task group
2. Parallel gateways can be run in two ways
    2.1 Coroutine mode This main mode of operation is the use of coroutine mode to run, mainly for io dense row data
    2.2 Process approach This is a true parallel, mainly aimed at computation intensive
3. The parallel gateway is actually an encapsulation of a task set, in which only ordinary tasks can be run
4. Parallel tasks can be combined in two ways
    4.1: Declarative: The id of the task group is declared in parallel tasks, that is, the id of the task group is
    declared in parallel_task_ids, which is declared at creation time
    4.2: Search: for all the task ids in the parallel task, let the framework find the task group itself,
        but the task must have pre_id and next_id
"""
from typing import List

import gevent

from conf.config import OrderLinesConfig
from orderlines.libraries.BaseTask import BaseTask
from orderlines.libraries.Group import GroupParam
from orderlines.task_running.process_runner import ProcessRunner

from orderlines.utils.base_orderlines_type import ParallelParam, ParallelResult
from orderlines.utils.parallel_util import ParallelUtils
from orderlines.utils.utils import get_current_node


class Parallel(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self, process_info, task_nodes):
        super(Parallel, self).__init__()
        self.process_info = process_info
        self.task_nodes = task_nodes
        self.parallel_helper = ParallelUtils(self.task_nodes)

    def _check_is_group(self, parallel_task_id: List[str]) -> bool:
        for task_id in parallel_task_id:
            current_node = get_current_node(task_id, self.task_nodes)
            if current_node.get('task_type') == 'group':
                return True
        return False

    def _get_group(self, parallel_task_id: List[str]) -> List[str]:
        """
        并行任务的第二种运行方式，是让框架自己帮你寻找任务组
        The second way to run parallel tasks is to let the framework find task groups for you
        :param parallel_task_id: task id
        :return:
        """
        flag = self._check_is_group(parallel_task_id)
        if flag:
            return parallel_task_id
        else:
            return self.parallel_helper.get_group_id(parallel_task_id)

    def _build_group_task(self, group_id: list, parallel_type: ParallelParam) -> dict:
        """
        获取的任务组
        The task group is obtained
        :param group_id:task group id
        :return:
        """
        for node in self.task_nodes:
            if node.get('task_id') == group_id:
                group_ids = node.get('method_kwargs').get('group_ids')
                from orderlines.libraries.Group import Group
                group = Group(self.process_info, self.task_nodes)
                current_node = get_current_node(parallel_type.task_id, parallel_type.task_nodes)
                param = {
                    'group_ids': group_ids,
                    'process_name': parallel_type.process_info.process_name,
                    'process_info': parallel_type.process_info,
                    'task_nodes': parallel_type.task_nodes,
                    'process_id': parallel_type.process_info.process_id,
                    'task_id': parallel_type.task_id,
                    'result': current_node.get('result'),
                    'task_config': current_node.get('task_config'),
                }
                group_param = GroupParam(**param)
                return group.task_group(group_param)

    def parallel_task(self, parallel_type: ParallelParam) -> ParallelResult:
        """
        并行网关
        运行并行任务组
        Run parallel task groups
        :param parallel_type:parallel task param type
        :return:
        """
        task_config = parallel_type.task_config
        parallel_task_ids = self._get_group(parallel_type.parallel_task_ids)
        runner_type = task_config.get('runner')
        if runner_type == 'process':
            return self._parallel_by_process(parallel_task_ids, task_config, parallel_type)
        else:
            return self._parallel_by_gevent(parallel_task_ids, task_config, parallel_type)

    def _parallel_by_gevent(
            self,
            parallel_task_ids: list,
            task_config: dict,
            parallel_type: str
    ) -> dict:
        """
        使用gevent协程并行
        Use gevent to realize parallel
        :param parallel_task_ids:parallel task ids
        :param task_config:Task configuration info
        :return:
        """
        timeout = task_config.get('timeout')
        timeout = timeout if timeout else OrderLinesConfig.task_timeout
        jobs = [gevent.spawn(self._build_group_task, group_ids, parallel_type) for group_ids in parallel_task_ids]
        gevent.joinall(jobs, timeout=timeout)
        return {parallel_task_ids[index]: job.value for index, job in enumerate(jobs)}

    def _parallel_by_process(
            self,
            parallel_task_ids: List[str],
            task_config: dict,
            parallel_type: str
    ) -> dict:
        """
        使用进程的方式并行，这主要适用计算密集型
        Use a process approach to parallelism, which is mainly suitable for computation intensive
        :param parallel_task_ids: parallel task ids
        :param task_config: Task configuration info
        :return:
        """
        pool_size = task_config.get('pool_size')
        timeout = task_config.get('timeout')
        process_runner = ProcessRunner(pool_size)
        return process_runner.spawn(self._build_group_task, parallel_task_ids, parallel_type, timeout)

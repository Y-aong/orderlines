# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : parallel_util.py
# Time       ：2023/3/5 14:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：
并行任务组中寻找任务组，这是并行任务组中的第二种方式，
就是并行任务组中给定的是所有的task下，需要框架自己需要找到任务组
其实可以算得上一个算法题
给定两个数组如下，

Look for task groups in parallel task groups, this is the second way in parallel task groups,
The parallel task group is given for all tasks, and the framework itself needs to find the task group
It's actually an algorithm problem
Given two arrays as follows,
data = [
    {
        'task_id': 1001,
        'prev_id': 1000,
        'next_id': 1002
    },
    {
        'task_id': 1002,
        'prev_id': 1001,
        'next_id': 1009
    },
    {
        'task_id': 1003,
        'prev_id': 1000,
        'next_id': 1004
    },
    {
        'task_id': 1004,
        'prev_id': 1003,
        'next_id': 1005
    },
    {
        'task_id': 1005,
        'prev_id': 1004,
        'next_id': 1009
    },
    {
        'task_id': 1006,
        'prev_id': 1000,
        'next_id': 1007
    },
    {
        'task_id': 1007,
        'prev_id': 1006,
        'next_id': 1009
    },
    {
        'task_id': 1008,
        'prev_id': 1000,
        'next_id': 1009
    },
]
parallel_task = [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008]
要求需找到group_ids = [[1001, 1002], [1003, 1004, 1005], [1006, 1007], [1008]]
"""
import copy
from typing import List

from orderlines.utils.utils import get_current_node


class ParallelUtils:
    def __init__(self, nodes: List[dict]):
        self.nodes = nodes
        self.result = list()

    def solution(
            self,
            task_id: str,
            parallel_task_ids: List[str],
            group_ids: List[str]
    ) -> None:
        """
        并行网关中参数，这里的task_id为普通任务节点的task_id
        Parameter of parallel gateway, where task_id is the task_id of a common task node
        :param task_id: task id
        :param parallel_task_ids:parallel task ids
        :param group_ids: task group id
        :return:
        """
        group_ids = copy.deepcopy(group_ids)
        current_node = get_current_node(task_id, self.nodes)
        prev_id = current_node.get('prev_id')
        next_id = current_node.get('next_id')
        # 寻找开始节点
        if task_id not in group_ids and prev_id not in parallel_task_ids:
            group_ids.append(task_id)
            parallel_task_ids.remove(task_id)

        if next_id not in parallel_task_ids and group_ids:
            # 终止条件. end condition
            self.result.append(group_ids)
            return
        # 节点的下一个节点在并行任务组中. The next node of the node is in the parallel task group
        if next_id in parallel_task_ids:
            group_ids.append(next_id)
            self.solution(next_id, parallel_task_ids, group_ids)

    def get_group_id(self, parallel_ids) -> List[list]:
        for task_id in parallel_ids:
            self.solution(task_id, parallel_ids, [])
        return self.result

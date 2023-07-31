# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : get_group_ids_test.py
# Time       ：2023/3/5 14:34
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from orderlines.utils.parallel_util import ParallelUtils


def get_group_ids():
    data = [
        {
            'task_id': "1001",
            'prev_id': "1000",
            'next_id': "1002"
        },
        {
            'task_id': "1002",
            'prev_id': "1001",
            'next_id': "1009"
        },
        {
            'task_id': "1003",
            'prev_id': "1000",
            'next_id': "1004"
        },
        {
            'task_id': "1004",
            'prev_id': "1003",
            'next_id': "1005"
        },
        {
            'task_id': "1005",
            'prev_id': "1004",
            'next_id': "1009"
        },
        {
            'task_id': '1006',
            'prev_id': '1000',
            'next_id': '1007'
        },
        {
            'task_id': '1007',
            'prev_id': '1006',
            'next_id': '1009'
        },
        {
            'task_id': '1008',
            'prev_id': '1000',
            'next_id': '1009'
        },
    ]
    parallel_task = ['1001', '1002', '1003', '1004', '1005', '1006', '1007', '1008']
    ret = ParallelUtils(data).get_group_id(parallel_task)
    print(ret)


if __name__ == '__main__':
    get_group_ids()

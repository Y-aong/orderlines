# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : demo.py
# Time       ：2023/9/19 15:55
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
import json

from data.flow import data

nodes = data.get('nodes')
edges = data.get('edges')

process = list()
for node in nodes:
    item = {}
    task_id = node.get('id')
    task_name = node.get('text').get('value')
    item['task_id'] = task_id
    item['task_name'] = task_name
    prev_id = list()
    next_id = list()

    for edge in edges:
        if edge.get('targetNodeId') == task_id:
            prev_id.append(edge.get('targetNodeId'))

        if edge.get('sourceNodeId') == task_id:
            next_id.append(edge.get('sourceNodeId'))

    item['prev_id'] = ','.join(prev_id) if prev_id else None
    item['next_id'] = ','.join(next_id) if next_id else None
    process.append(item)

print(process)

# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : demo.py
# Time       ：2023/9/19 15:55
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""

data = [
    {
        "expression": "142231 > 231412; 142231 = 341243; ",
        "condition_name": "ae69de5d-e125-4eb6-b1c6-0a007af15b48",
        "conditions": [
            {
                "condition": "142231",
                "target": "231412",
                "sign": ">"
            },
            {
                "condition": "142231",
                "target": "341243",
                "sign": "="
            }
        ]
    },
    {
        "expression": "142231 < 34124; ",
        "condition_name": "d6d9a4ac-bf4b-49e3-9e49-e116f12a735e",
        "conditions": [
            {
                "condition": "142231",
                "target": "34124",
                "sign": "<"
            }
        ]
    }
]
method_kwargs = {}
conditions = list()
expression = list()
for item in data:
    condition_name = item.get('condition_name')
    conditions.append({
        'task_id': condition_name,
        'conditions': item.get('conditions')
    })
    expression.append({'task_id': condition_name})

method_kwargs['conditions'] = conditions
method_kwargs['expression'] = expression

print(method_kwargs)

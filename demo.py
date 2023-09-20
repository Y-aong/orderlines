# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : demo.py
# Time       ：2023/9/19 15:55
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""

data = {
    "nodes": [
        {
            "id": "17d69720-1963-426a-bccd-f3e1f5d7e708",
            "type": "start-node",
            "x": 1060,
            "y": 30,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "start",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 1060,
                "y": 30,
                "value": "开始节点"
            }
        },
        {
            "id": "64569a66-43f0-4d05-aae5-bf95428a1749",
            "type": "end-node",
            "x": 1070,
            "y": 510,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "end",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 1070,
                "y": 510,
                "value": "结束节点"
            }
        },
        {
            "id": "aaf2c34c-e3af-4667-8b31-1a3584379d03",
            "type": "process-control-node",
            "x": 1060,
            "y": 200,
            "properties": {
                "class_name": "ProcessControl",
                "method_name": "process_control",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 1060,
                "y": 200,
                "value": "流程控制"
            }
        },
        {
            "id": "334273ba-5a7b-47cf-b53c-34978f1f81eb",
            "type": "function-node",
            "x": 940,
            "y": 340,
            "properties": {
                "method_name": "test_subtraction",
                "class_name": "Test",
                "version": "1.0.0.1",
                "ui": "orderlines-node"
            },
            "text": {
                "x": 940,
                "y": 340,
                "value": "减法测试"
            }
        },
        {
            "id": "259deb61-539f-4e0b-b7a5-39575f0fc291",
            "type": "function-node",
            "x": 1180,
            "y": 340,
            "properties": {
                "method_name": "test_subtraction",
                "class_name": "Test",
                "version": "1.0.0.1",
                "ui": "orderlines-node"
            },
            "text": {
                "x": 1180,
                "y": 340,
                "value": "减法测试"
            }
        }
    ],
    "edges": [
        {
            "id": "c9df0cb7-d439-4f15-b9f2-94d715890c91",
            "type": "flow-link",
            "sourceNodeId": "aaf2c34c-e3af-4667-8b31-1a3584379d03",
            "targetNodeId": "334273ba-5a7b-47cf-b53c-34978f1f81eb",
            "startPoint": {
                "x": 1060,
                "y": 245
            },
            "endPoint": {
                "x": 940,
                "y": 310
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 1060,
                    "y": 245
                },
                {
                    "x": 1060,
                    "y": 280
                },
                {
                    "x": 940,
                    "y": 280
                },
                {
                    "x": 940,
                    "y": 310
                }
            ]
        },
        {
            "id": "ff1e7f34-eb3a-4627-bd5c-cd730477acb2",
            "type": "flow-link",
            "sourceNodeId": "aaf2c34c-e3af-4667-8b31-1a3584379d03",
            "targetNodeId": "259deb61-539f-4e0b-b7a5-39575f0fc291",
            "startPoint": {
                "x": 1060,
                "y": 245
            },
            "endPoint": {
                "x": 1180,
                "y": 310
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 1060,
                    "y": 245
                },
                {
                    "x": 1060,
                    "y": 280
                },
                {
                    "x": 1180,
                    "y": 280
                },
                {
                    "x": 1180,
                    "y": 310
                }
            ]
        },
        {
            "id": "8e060d89-0db4-402b-b7ca-09660a023536",
            "type": "flow-link",
            "sourceNodeId": "334273ba-5a7b-47cf-b53c-34978f1f81eb",
            "targetNodeId": "64569a66-43f0-4d05-aae5-bf95428a1749",
            "startPoint": {
                "x": 940,
                "y": 370
            },
            "endPoint": {
                "x": 1034,
                "y": 510
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 940,
                    "y": 370
                },
                {
                    "x": 940,
                    "y": 510
                },
                {
                    "x": 1034,
                    "y": 510
                }
            ]
        },
        {
            "id": "395603b2-7e69-4cfc-bf1c-b28a481dffd2",
            "type": "flow-link",
            "sourceNodeId": "259deb61-539f-4e0b-b7a5-39575f0fc291",
            "targetNodeId": "64569a66-43f0-4d05-aae5-bf95428a1749",
            "startPoint": {
                "x": 1180,
                "y": 370
            },
            "endPoint": {
                "x": 1106,
                "y": 510
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 1180,
                    "y": 370
                },
                {
                    "x": 1180,
                    "y": 510
                },
                {
                    "x": 1106,
                    "y": 510
                }
            ]
        },
        {
            "id": "133dda29-d2bd-4ad5-85df-4317e71f5eba",
            "type": "flow-link",
            "sourceNodeId": "17d69720-1963-426a-bccd-f3e1f5d7e708",
            "targetNodeId": "aaf2c34c-e3af-4667-8b31-1a3584379d03",
            "startPoint": {
                "x": 1060,
                "y": 66
            },
            "endPoint": {
                "x": 1060,
                "y": 155
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 1060,
                    "y": 66
                },
                {
                    "x": 1060,
                    "y": 155
                }
            ]
        }
    ]
}

nodes = data.get('nodes')
edges = data.get('edges')
task_id = 'aaf2c34c-e3af-4667-8b31-1a3584379d03'


def get_task_name(source_task_id):
    for node in nodes:
        if node.get('id') == source_task_id:
            return node.get('text').get('value')
    return None


items = []
for edge in edges:
    if edge.get('sourceNodeId') == task_id:
        items.append(
            {
                'label': get_task_name(edge.get('targetNodeId')),
                'value': edge.get('targetNodeId')
            }
        )

print(items)

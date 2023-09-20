# !/usr/bin/env python
# -*-coding:utf-8 -*-
data = {
    "nodes": [
        {
            "id": "17d69720-1963-426a-bccd-f3e1f5d7e708",
            "type": "start-node",
            "x": 600,
            "y": -200,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "start",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 600,
                "y": -200,
                "value": "开始节点"
            }
        },
        {
            "id": "64569a66-43f0-4d05-aae5-bf95428a1749",
            "type": "end-node",
            "x": 600,
            "y": 230,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "end",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 600,
                "y": 230,
                "value": "结束节点"
            }
        },
        {
            "id": "7a33a13a-8b44-44b9-8956-ef0a865ac866",
            "type": "function-node",
            "x": 600,
            "y": -90,
            "properties": {
                "class_name": "Test",
                "method_name": "test_subtraction",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 600,
                "y": -90,
                "value": "减法测试"
            }
        },
        {
            "id": "337df460-b9b5-4380-8db3-896e84a5cbe8",
            "type": "function-node",
            "x": 600,
            "y": 10,
            "properties": {
                "class_name": "Test",
                "method_name": "test_multi",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 600,
                "y": 10,
                "value": "乘法测试"
            }
        },
        {
            "id": "46eba828-f15d-4856-9d0f-b11f935eeb05",
            "type": "function-node",
            "x": 600,
            "y": 110,
            "properties": {
                "class_name": "Test",
                "method_name": "test_add",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 600,
                "y": 110,
                "value": "加法测试"
            }
        }
    ],
    "edges": [
        {
            "id": "4972b168-83e1-4459-a9d4-f0c5ee4a0d19",
            "type": "flow-link",
            "sourceNodeId": "17d69720-1963-426a-bccd-f3e1f5d7e708",
            "targetNodeId": "7a33a13a-8b44-44b9-8956-ef0a865ac866",
            "startPoint": {
                "id": "600--164",
                "x": 600,
                "y": -164
            },
            "endPoint": {
                "x": 600,
                "y": -120
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 600,
                    "y": -164
                },
                {
                    "x": 600,
                    "y": -120
                }
            ]
        },
        {
            "id": "f23b0a73-27d0-4475-8a2a-58213199922d",
            "type": "flow-link",
            "sourceNodeId": "7a33a13a-8b44-44b9-8956-ef0a865ac866",
            "targetNodeId": "337df460-b9b5-4380-8db3-896e84a5cbe8",
            "startPoint": {
                "x": 600,
                "y": -60
            },
            "endPoint": {
                "x": 600,
                "y": -20
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 600,
                    "y": -60
                },
                {
                    "x": 600,
                    "y": -20
                }
            ]
        },
        {
            "id": "6507b4d2-7715-4d22-b156-1f1947ed89bd",
            "type": "flow-link",
            "sourceNodeId": "337df460-b9b5-4380-8db3-896e84a5cbe8",
            "targetNodeId": "46eba828-f15d-4856-9d0f-b11f935eeb05",
            "startPoint": {
                "x": 600,
                "y": 40
            },
            "endPoint": {
                "x": 600,
                "y": 80
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 600,
                    "y": 40
                },
                {
                    "x": 600,
                    "y": 70
                },
                {
                    "x": 600,
                    "y": 70
                },
                {
                    "x": 600,
                    "y": 50
                },
                {
                    "x": 600,
                    "y": 50
                },
                {
                    "x": 600,
                    "y": 80
                }
            ]
        },
        {
            "id": "607dcd57-1de1-44bf-93d6-69de25c02393",
            "type": "flow-link",
            "sourceNodeId": "46eba828-f15d-4856-9d0f-b11f935eeb05",
            "targetNodeId": "64569a66-43f0-4d05-aae5-bf95428a1749",
            "startPoint": {
                "x": 600,
                "y": 140
            },
            "endPoint": {
                "id": "600-134",
                "x": 600,
                "y": 194
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 600,
                    "y": 140
                },
                {
                    "x": 600,
                    "y": 170
                },
                {
                    "x": 600,
                    "y": 170
                },
                {
                    "x": 600,
                    "y": 164
                },
                {
                    "x": 600,
                    "y": 164
                },
                {
                    "x": 600,
                    "y": 194
                }
            ]
        }
    ]
}

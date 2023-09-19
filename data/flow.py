# !/usr/bin/env python
# -*-coding:utf-8 -*-
data = {
    "nodes": [
        {
            "id": "dccd1479-b63d-4185-ac11-b1741cfa622d",
            "type": "process-control-node",
            "x": 830,
            "y": -890,
            "properties": {
                "class_name": "ProcessControl",
                "method_name": "process_control",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 830,
                "y": -890,
                "value": "流程控制"
            },
        },
        {
            "id": "81d4bebb-4227-4bfe-8feb-0f863a542f5c",
            "type": "parallel-node",
            "x": 830,
            "y": -740,
            "properties": {
                "class_name": "Parallel",
                "method_name": "parallel_task",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 830,
                "y": -740,
                "value": "并行网关"
            }
        },
        {
            "id": "adfb7c2f-08a2-4564-80a4-d27f81580111",
            "type": "start-node",
            "x": 830,
            "y": -1040,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "start",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 830,
                "y": -1040,
                "value": "开始节点"
            }
        },
        {
            "id": "e531220d-fcc2-418f-b01c-e818ba80a3b1",
            "type": "function-node",
            "x": 690,
            "y": -570,
            "properties": {
                "class_name": "Test",
                "method_name": "test_subtraction",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 690,
                "y": -570,
                "value": "减法测试"
            }
        },
        {
            "id": "a4270896-516b-429d-b26f-43ac448f6d54",
            "type": "function-node",
            "x": 980,
            "y": -570,
            "properties": {
                "class_name": "Test",
                "method_name": "test_multi",
                "ui": "orderlines-node",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 980,
                "y": -570,
                "value": "乘法测试"
            }
        },
        {
            "id": "2bc165be-9e99-44ff-85d5-46ab7507dacc",
            "type": "end-node",
            "x": 840,
            "y": -320,
            "properties": {
                "class_name": "BuiltIn",
                "method_name": "end",
                "version": "1.0.0.1"
            },
            "text": {
                "x": 840,
                "y": -320,
                "value": "结束节点"
            }
        }
    ],
    "edges": [
        {
            "id": "832ba872-d41d-4661-9daf-e0d03bcb84af",
            "type": "flow-link",
            "sourceNodeId": "adfb7c2f-08a2-4564-80a4-d27f81580111",
            "targetNodeId": "dccd1479-b63d-4185-ac11-b1741cfa622d",
            "startPoint": {
                "x": 830,
                "y": -1004
            },
            "endPoint": {
                "x": 830,
                "y": -935
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 830,
                    "y": -1004
                },
                {
                    "x": 830,
                    "y": -935
                }
            ]
        },
        {
            "id": "74185e26-a80f-4df9-9dea-4389f9ea25f6",
            "type": "flow-link",
            "sourceNodeId": "dccd1479-b63d-4185-ac11-b1741cfa622d",
            "targetNodeId": "81d4bebb-4227-4bfe-8feb-0f863a542f5c",
            "startPoint": {
                "x": 830,
                "y": -845
            },
            "endPoint": {
                "x": 830,
                "y": -770
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 830,
                    "y": -845
                },
                {
                    "x": 830,
                    "y": -770
                }
            ]
        },
        {
            "id": "bc543feb-0b1b-4007-a119-d383791856a7",
            "type": "flow-link",
            "sourceNodeId": "81d4bebb-4227-4bfe-8feb-0f863a542f5c",
            "targetNodeId": "e531220d-fcc2-418f-b01c-e818ba80a3b1",
            "startPoint": {
                "x": 830,
                "y": -710
            },
            "endPoint": {
                "x": 690,
                "y": -600
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 830,
                    "y": -710
                },
                {
                    "x": 830,
                    "y": -630
                },
                {
                    "x": 690,
                    "y": -630
                },
                {
                    "x": 690,
                    "y": -600
                }
            ]
        },
        {
            "id": "12380dd0-e201-4fd8-a2b3-6d97d2ad3d24",
            "type": "flow-link",
            "sourceNodeId": "81d4bebb-4227-4bfe-8feb-0f863a542f5c",
            "targetNodeId": "a4270896-516b-429d-b26f-43ac448f6d54",
            "startPoint": {
                "x": 830,
                "y": -710
            },
            "endPoint": {
                "x": 980,
                "y": -600
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 830,
                    "y": -710
                },
                {
                    "x": 830,
                    "y": -630
                },
                {
                    "x": 980,
                    "y": -630
                },
                {
                    "x": 980,
                    "y": -600
                }
            ]
        },
        {
            "id": "890321ee-f2be-46b5-8913-56456871c79a",
            "type": "flow-link",
            "sourceNodeId": "e531220d-fcc2-418f-b01c-e818ba80a3b1",
            "targetNodeId": "2bc165be-9e99-44ff-85d5-46ab7507dacc",
            "startPoint": {
                "x": 690,
                "y": -540
            },
            "endPoint": {
                "x": 804,
                "y": -320
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 690,
                    "y": -540
                },
                {
                    "x": 690,
                    "y": -320
                },
                {
                    "x": 804,
                    "y": -320
                }
            ]
        },
        {
            "id": "8010d965-6a1f-4950-b63c-9295f9b35d13",
            "type": "flow-link",
            "sourceNodeId": "a4270896-516b-429d-b26f-43ac448f6d54",
            "targetNodeId": "2bc165be-9e99-44ff-85d5-46ab7507dacc",
            "startPoint": {
                "x": 980,
                "y": -540
            },
            "endPoint": {
                "x": 876,
                "y": -320
            },
            "properties": {},
            "pointsList": [
                {
                    "x": 980,
                    "y": -540
                },
                {
                    "x": 980,
                    "y": -320
                },
                {
                    "x": 876,
                    "y": -320
                }
            ]
        }
    ]
}

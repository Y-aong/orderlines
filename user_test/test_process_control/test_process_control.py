# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : test_process_control.py
# Time       ：2023/8/14 11:46
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
import pytest
from orderlines.libraries.ProcessControl import ProcessControl
from orderlines.utils.base_orderlines_type import ProcessControlParam


def test_process_control_by_return():
    task_config = {
        'timeout': 120,
        'task_strategy': 'RAISE',
        'retry_time': 3,
        'notice_type': 'FAILURE',
        'callback_func': 'send_msg',
        'callback_module': 'Email'
    }
    pc_type = 'result',
    conditions = [
        {
            'task_id': '1014',
            'condition': [
                {'sign': '=', 'target': 788, 'condition': 1},
                {'sign': '>', 'target': 3, 'condition': 1}
            ]
        },
        {
            'task_id': '1015',
            'condition': [
                {'sign': '<', 'target': 788, 'condition': 2},
                {'sign': '=', 'target': 3, 'condition': 3}
            ]
        }
    ]
    process_info = {
        'process_config': None,
        'creator': 'blue',
        'process_id': '1007',
        'desc': None,
        'process_params': None,
        'process_name': 'test_process_return',
        'updater': None,
        'process_instance_id': 'ff54c4fb378e11eebef7001a7dda7111'
    }
    data = {
        'task_config': task_config,
        'pc_type': pc_type,
        'conditions': conditions,
        'process_info': process_info,
    }
    task_id = ProcessControl().process_control(ProcessControlParam(**data))
    assert task_id == '1015'


def test_process_control_by_status():
    process_control = {
        'task_config': {
            'timeout': 120,
            'task_strategy': 'RAISE',
            'retry_time': 3,
            'notice_type': 'FAILURE',
            'callback_func': 'send_msg',
            'callback_module': 'Email'
        },
        'pc_type': 'status',
        'conditions': [
            {
                'task_id': '1014',
                'condition': [{'task_status': 'success', 'condition': '1012'}]
            },
            {
                'task_id': '1015',
                'condition': [{'task_status': 'failure', 'condition': '1012'}]
            }
        ],
        'process_info': {
            'updater': None,
            'desc': None,
            'active': 1,
            'process_params': None,
            'process_config': None,
            'process_name': 'test_process_status',
            'creator': 'blue',
            'process_id': '1008',
            'process_instance_id': '8d37e9af3a6411ee910a2811a804f5ff'
        }
    }
    task_id = ProcessControl().process_control(ProcessControlParam(**process_control))
    assert task_id == '1015'


if __name__ == '__main__':
    pytest.main()

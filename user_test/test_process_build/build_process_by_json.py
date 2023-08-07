# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : build_process_by_json.py
# Time       ：2023/7/30 15:31
# Author     ：Y-aong
# version    ：python 3.7
# Description：通过json构建流程
"""
from orderlines.utils.process_build_adapter import ProcessBuildAdapter


def build_process_by_json():
    json_path = './data/process.json'
    process_info, task_nodes = ProcessBuildAdapter().build_by_json(json_path)
    print(process_info)


build_process_by_json()

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : build_process_by_yaml.py
# Time       ：2023/7/30 15:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：根据yaml文件构建流程
"""
import json

import yaml

from order_lines.utils.process_build_adapter import ProcessBuildAdapter


def build_process_by_yaml():
    json_path = './data/process.yaml'
    process_info, task_nodes = ProcessBuildAdapter().read_yaml(json_path)
    print(process_info)


build_process_by_yaml()

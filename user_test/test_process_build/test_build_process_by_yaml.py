# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_build_process_by_yaml.py
# Time       ：2023/7/30 15:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：根据yaml文件构建流程
"""
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter


def test_build_process_by_yaml():
    json_path = './data/process.yaml'
    table_id = ProcessBuildAdapter().build_by_yaml(json_path, clear_db=True)
    assert table_id

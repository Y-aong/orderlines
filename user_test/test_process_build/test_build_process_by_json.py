# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_build_process_by_json.py
# Time       ：2023/7/30 15:31
# Author     ：Y-aong
# version    ：python 3.7
# Description：通过json构建流程
"""
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter


def test_build_process_by_json():
    json_path = './data/process.json'
    process_id = ProcessBuildAdapter().build_by_json(json_path, clear_db=True)
    assert process_id

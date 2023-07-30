# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : build_process_by_sql.py
# Time       ：2023/7/30 15:40
# Author     ：Y-aong
# version    ：python 3.7
# Description：根据数据库数据构建流程
"""
from order_lines.utils.process_build_adapter import ProcessBuildAdapter


def build_process_by_sql():
    process_info, task_nodes = ProcessBuildAdapter().read_sql(process_id=2)
    print(process_info)


build_process_by_sql()

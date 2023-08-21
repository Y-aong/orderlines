# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : run_by_process_id.py
# Time       ：2023/8/16 22:42
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from orderlines import OrderLines
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter


def run_by_process_id_test():
    json_path = './data/process.json'
    process_id = ProcessBuildAdapter().build_by_json(json_path, clear_db=True)
    orderlines = OrderLines()
    orderlines.start(process_id=process_id)


if __name__ == '__main__':
    run_by_process_id_test()

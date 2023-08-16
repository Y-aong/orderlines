# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_run_by_process_id.py
# Time       ：2023/8/16 22:42
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from orderlines import OrderLines


def test_run_by_process_id():
    process_id = 134
    orderlines = OrderLines()
    orderlines.start(process_id=process_id)


test_run_by_process_id()

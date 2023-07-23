# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : by_process_id_test.py
# Time       ：2023/3/12 14:30
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""

from order_lines import OrderLines
from public.order_lines_helper import OrderLinesHelper

if __name__ == "__main__":
    process = OrderLinesHelper('1001').get_process()
    OrderLines(**process).run()

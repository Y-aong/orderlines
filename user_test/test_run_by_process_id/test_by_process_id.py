# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_by_process_id.py
# Time       ：2023/3/12 14:30
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app.public.order_lines_helper import OrderLinesHelper
from order_lines import OrderLines

if __name__ == "__main__":
    process = OrderLinesHelper('1001').get_process()
    OrderLines(**process).run()

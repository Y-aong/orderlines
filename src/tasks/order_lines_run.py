# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_run.py
# Time       ：2023/7/8 10:37
# Author     ：Y-aong
# version    ：python 3.7
# Description：order_lines celery方法入口
"""
from apis import celery
from public.order_lines_helper import OrderLinesHelper
from order_lines import OrderLines


@celery.task(name='order_lines_run')
def order_lines_run(process_id):
    process = OrderLinesHelper(process_id).get_process()
    OrderLines(**process).run()

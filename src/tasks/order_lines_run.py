# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_run.py
# Time       ：2023/3/12 14:46
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app import celery
from flask_app.public.order_lines_helper import OrderLinesHelper
from order_lines import OrderLines


@celery.task(name='order_lines_run')
def order_lines_run(process_id):
    process = OrderLinesHelper(process_id).get_process()
    OrderLines(**process).run()



# import gevent
#
# jobs = [gevent.spawn(order_lines_run, i )for i in ['1001', '1001']]
# gevent.joinall(jobs)

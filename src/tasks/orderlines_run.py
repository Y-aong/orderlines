# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_run.py
# Time       ：2023/7/8 10:37
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines celery方法入口
    orderlines celery method enter point
"""
from celery.signals import before_task_publish

from apis import celery
from orderlines import OrderLines


@before_task_publish.connect(sender='orderlines_run')
def orderlines_check(headers=None, body=None, **kwargs):
    _, params, _ = body
    process_id = params.get('process_id')
    print(f'process_id::{process_id}')


@celery.task(name='orderlines_run')
def orderlines_run(process_id):
    OrderLines().start(process_id=process_id)

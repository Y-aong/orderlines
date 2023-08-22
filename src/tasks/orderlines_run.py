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
from typing import Union

from celery.signals import before_task_publish
from apis import celery
from public.logger import logger


@before_task_publish.connect(sender='orderlines_run')
def orderlines_check(headers=None, body=None, **kwargs):
    from public.schedule_utils.schedule_check import ScheduleCheck
    _, params, _ = body
    process_id = params.get('process_id')
    run_type = params.get('run_type')
    schedule_check = ScheduleCheck()
    stop_schedule = schedule_check.check_schedule_task()
    is_available = schedule_check.check_schedule_task_is_available(process_id)
    if not stop_schedule and run_type == 'schedule':
        logger.info(
            'Main switch of scheduled task is closed, if you want stop schedule task,'
            'please update table base_config config_name is stop_all_schedule,'
            'set config_value 1')
    if not is_available and run_type == 'schedule':
        logger.info(
            'schedule task run time is not in available datetime, but you can start by'
            'trigger not schedule, or change invalid_start_time, invalid_end_time '
        )


@celery.task(name='orderlines_run')
def orderlines_run(process_id, run_type='schedule'):
    from orderlines import OrderLines
    OrderLines().start(process_id=process_id, run_type=run_type)


def orderlines_schedule_run(process_id: Union[str, int], run_type: str):
    orderlines_run.delay(process_id=process_id, run_type=run_type)

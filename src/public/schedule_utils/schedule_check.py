# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_check.py
# Time       ：2023/8/16 22:31
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    检查定时
    check schedule
"""
from datetime import datetime

from apis.config.models import BaseConfig
from apis.orderlines.models import ScheduleTask
from apis.config.schema.base_config_schema import BaseConfigSchema
from apis.orderlines.schema.schedule_task_schema import ScheduleTaskSchema
from public.base_model import get_session


class ScheduleCheck:
    def __init__(self):
        self.session = get_session()

    def check_schedule_task(self) -> bool:
        """检查定时任务总开关"""
        obj = self.session.query(BaseConfig).filter(
            BaseConfig.config_name == 'stop_all_schedule',
            BaseConfig.active == 1
        ).first()
        config_info = BaseConfigSchema().dump(obj)
        stop_all_schedule = config_info.get('config_value')
        return stop_all_schedule == '1'

    def check_schedule_task_is_available(self, process_id) -> bool:
        """检查定时任务是否在可用时间"""
        obj = self.session.query(ScheduleTask).filter(
            ScheduleTask.process_id == process_id,
            ScheduleTask.active == 1
        ).first()
        schedule_task = ScheduleTaskSchema().dump(obj)
        invalid_start_time = schedule_task.get('invalid_start_time')
        invalid_end_time = schedule_task.get('invalid_end_time')
        invalid_start_datetime = datetime.strptime(invalid_start_time, '%Y-%m-%d %H-%M-%S')
        invalid_end_datetime = datetime.strptime(invalid_end_time, '%Y-%m-%d %H-%M-%S')
        curren_datetime = datetime.now()
        return invalid_start_datetime <= curren_datetime <= invalid_end_datetime

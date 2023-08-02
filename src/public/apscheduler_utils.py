# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : apscheduler_utils.py
# Time       ：2023/6/29 10:58
# Author     ：YangYong
# version    ：python 3.10
# Description：
    定时计划的增删改查
    Schedule additions, deletions, corrections and checks
"""
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger

from apis.schedule_plan.models.schedule_plan_models import ApschedulerJobs
from public.apscheduler_config import scheduler
from public.base_model import get_session


def demo(process_name: str, exe_type: str):
    print(f'this is a test::{process_name}, {exe_type}')


class ApschedulerUtils:
    def __init__(self):
        self.exe_type = 'schedule'
        self.cron_key = ['year', 'month', 'day', 'week', 'day_of_week', 'hour', 'minute', 'second']
        self.interval_key = ['weeks', 'days', 'hours', 'minutes', 'seconds']
        self.date_key = ['run_date']
        self.session = get_session()
        self.schedule_keys = {
            'interval': self.interval_key,
            'cron': self.cron_key,
            'date': self.date_key
        }
        self.target_func = demo

    def check_param(self, param: dict, trigger: str) -> dict:
        data = dict()
        schedule_key = self.schedule_keys.get(trigger)
        for key, val in param.items():
            if key in schedule_key:
                data.setdefault(key, val)
        return data

    def check_task(self, process_id: str) -> bool:
        """检查定时任务是否存在, Check whether scheduled tasks exist"""
        job = self.session.query(ApschedulerJobs).filter(ApschedulerJobs.id == process_id).first()
        return False if not job else True

    def get_schedule_task(self, process_id: str) -> dict:
        if self.check_task(process_id):
            schedule_info = scheduler.get_job(process_id)
            print(f'schedule_info::{schedule_info}')
            if schedule_info:
                return {
                    'next_run_time': schedule_info.next_run_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'method_name': schedule_info.func.__name__,
                    'name': schedule_info.name
                }

        return {}

    def create_schedule_task(
            self,
            trigger_type: str,
            process_id: str,
            process_name: str,
            **schedule_data
    ):
        """创建定时任务入口"""
        if trigger_type == 'interval':
            schedule_data = self.check_param(schedule_data, trigger_type)
        elif trigger_type == 'cron':
            schedule_data = self.check_param(schedule_data, trigger_type)
        elif trigger_type == 'date':
            schedule_data = self.check_param(schedule_data, trigger_type)
        else:
            raise ValueError(f'trigger::{trigger_type}Parameter error')
        scheduler.add_job(
            id=process_id,
            func=self.target_func,
            args=(process_id, self.exe_type),
            name=process_name,
            coalesce=True,
            replace_existing=True,
            trigger=trigger_type,
            **schedule_data
        )

    def update_schedule_task(
            self,
            trigger_type: str,
            process_id: str,
            **trigger_data
    ):
        """修改定时任务, update schedule task"""
        self.check_task(process_id)
        if trigger_type == 'interval':
            trigger_data = self.check_param(trigger_data, trigger_type)
            trigger_instance = IntervalTrigger(**trigger_data)
        elif trigger_type == 'cron':
            trigger_data = self.check_param(trigger_data, trigger_type)
            trigger_instance = CronTrigger(**trigger_data)
        elif trigger_type == 'date':
            trigger_data = self.check_param(trigger_data, trigger_type)
            trigger_instance = DateTrigger(**trigger_data)
        else:
            raise ValueError(f'trigger::{trigger_type}参数异常')

        scheduler.modify_job(job_id=process_id, trigger=trigger_instance)

    def delete_schedule_task(self, process_id: str):
        """删除定时任务,Deleting a Scheduled Task"""
        if self.check_task(process_id):
            scheduler.remove_job(process_id)
        raise ValueError(f'job id {process_id} not exist')

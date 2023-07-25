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
        from tasks.order_lines_run import order_lines_run
        self.target_func = order_lines_run

    def check_param(self, param, trigger):
        data = dict()
        schedule_key = self.schedule_keys.get(trigger)
        for key, val in param.items():
            if key in schedule_key:
                data.setdefault(key, val)
        return data

    def add_task(self, trigger_type, job_name, patrol_task_id, task_name, **schedule_data):
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
            id=job_name,
            func=self.target_func,
            args=(patrol_task_id, self.exe_type),
            name=task_name,
            coalesce=True,
            replace_existing=True,
            trigger=trigger_type,
            **schedule_data
        )

    def modify_task(self, trigger_type, job_id, args=None, **trigger_data):
        self.check_task(job_id)
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
        if args:
            scheduler.modify_job(job_id=job_id, trigger=trigger_instance, args=args)
        else:
            scheduler.modify_job(job_id=job_id, trigger=trigger_instance)

    def check_task(self, job_name):
        """检查定时任务是否存在, Check whether scheduled tasks exist"""
        job = self.session.query(ApschedulerJobs).filter(ApschedulerJobs.id == job_name).first()
        return False if not job else True

    def delete_task(self, job_id):
        """删除定时任务,Deleting a Scheduled Task"""
        if self.check_task(job_id):
            scheduler.remove_job(job_id)

    def get_task(self, job_name):
        if self.check_task(job_name):
            schedule_info = scheduler.get_job(job_name)
            if schedule_info:
                return {
                    'next_run_time': schedule_info.next_run_time.strftime('%Y-%m-%d %H:%M:%S'),
                    'func': schedule_info.func.__name__,
                    'args': schedule_info.args,
                    'kwargs': schedule_info.kwargs,
                    'name': schedule_info.name
                }
            else:
                return None

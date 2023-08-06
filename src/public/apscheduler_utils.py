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

    def check_plan(self, job_id: str) -> bool:
        """检查定时任务是否存在, Check whether scheduled tasks exist"""
        job = self.session.query(ApschedulerJobs).filter(ApschedulerJobs.id == job_id).first()
        return False if not job else True

    def get_schedule_plan(self, job_id: str) -> dict:
        schedule_plan = dict()
        if self.check_plan(job_id):

            schedule_info = scheduler.get_job(job_id)
            print(f'schedule_info::{schedule_info}')
            if schedule_info:
                schedule_plan.setdefault('next_run_time', schedule_info.next_run_time.strftime('%Y-%m-%d %H:%M:%S'))
                schedule_plan.setdefault('method_name', schedule_info.func.__name__)
                schedule_plan.setdefault('name', schedule_info.name)
            return schedule_plan

    def create_schedule_plan(
            self,
            trigger_type: str,
            job_id: str,
            process_name: str,
            **schedule_data
    ):
        """创建定时任务入口"""
        schedule_data.setdefault('timezone', 'Asia/Shanghai')
        if trigger_type == 'interval':
            schedule_data = self.check_param(schedule_data, trigger_type)
        elif trigger_type == 'cron':
            schedule_data = self.check_param(schedule_data, trigger_type)
        elif trigger_type == 'date':
            schedule_data = self.check_param(schedule_data, trigger_type)
        else:
            raise ValueError(f'trigger::{trigger_type}Parameter error')
        scheduler.add_job(
            id=job_id,
            func=self.target_func,
            args=(job_id, self.exe_type),
            name=process_name,
            coalesce=True,
            replace_existing=True,
            trigger=trigger_type,
            **schedule_data
        )

    def update_schedule_plan(
            self,
            trigger_type: str,
            job_id: str,
            **schedule_data
    ):
        """修改定时任务, update schedule task"""
        if self.check_plan(job_id):
            schedule_data.setdefault('timezone', 'Asia/Shanghai')
            schedule_plan = self.get_schedule_plan(job_id)
            self.delete_schedule_plan(job_id)
            self.create_schedule_plan(
                trigger_type=trigger_type,
                job_id=job_id,
                process_name=schedule_plan.get('name'),
                **schedule_data
            )

    def delete_schedule_plan(self, job_id: str):
        """删除定时任务,Deleting a Scheduled Task"""
        if self.check_plan(job_id):
            scheduler.remove_job(job_id)
        else:
            raise ValueError(f'job id {job_id} not exist')

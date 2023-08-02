# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : schedule_task_view.py
# Time       ：2023/8/2 15:20
# Author     ：YangYong
# version    ：python 3.10
# Description：
    定时任务视图类
    schedule task
"""
import json

from flask import request, current_app, url_for

from apis.orderlines.models import ScheduleTask, Process
from apis.orderlines.schema.schedule_task_schema import ScheduleTaskSchema
from apis.schedule_plan.models import DatePlan, IntervalPlan, CrontabPlan
from apis.schedule_plan.schema.schedule_plan_schema import CrontabPlanSchema, DatePlanSchema, IntervalPlanSchema
from public.base_model import db
from public.base_view import BaseView


class ScheduleTaskView(BaseView):
    url = '/schedule_task'

    def __init__(self):
        super(ScheduleTaskView, self).__init__()
        self.table_orm = ScheduleTask
        self.table_schema = ScheduleTaskSchema

        self.schedule_plan_orm = {
            'date': DatePlan,
            'interval': IntervalPlan,
            'crontab': CrontabPlan
        }

    def handle_filter(self):
        for key, val in self.form_data.items():
            if hasattr(self.table_orm, key):
                self.filter.append(getattr(self.table_orm, key) == val)
            elif key == 'start_time' and val:
                self.filter.append(self.table_orm.start_time >= val)
            elif key == 'end_time' and val:
                self.filter.append(self.table_orm.end_time <= val)

    @staticmethod
    def get_schedule_plan(trigger, schedule_plan_id):
        table_orms = {
            'cron': CrontabPlan,
            'date': DatePlan,
            'interval': IntervalPlan
        }
        table_schemas = {
            'cron': CrontabPlanSchema,
            'date': DatePlanSchema,
            'interval': IntervalPlanSchema
        }

        table_orm = table_orms.get(trigger)
        table_schema = table_schemas.get(trigger)
        if not table_orm or not table_schema:
            raise ValueError(f'trigger {trigger} is not invalid')
        data = dict()
        if table_orm:
            schedule_plan = db.session.query(table_orm).filter(table_orm.id == schedule_plan_id).first()
            schedule_plan = table_schema().dump(schedule_plan)
            for key, val in schedule_plan.items():
                if schedule_plan.get(key):
                    data.setdefault(key, val)
        return data

    def handle_schedule_item(self):
        if self.form_data.get('page') and self.form_data.get('pre_page'):
            for item in self.response_data.get('items'):
                schedule_plan_id = item.get('schedule_plan_id')
                trigger = item.get('trigger')
                schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
                item['schedule_plan'] = schedule_plan
        if isinstance(self.response_data, dict) and request.method == 'GET':
            trigger = self.response_data.get('trigger')
            schedule_plan_id = self.response_data.get('schedule_plan_id')
            schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
            self.response_data['schedule_plan'] = schedule_plan
        elif isinstance(self.response_data, list) and request.method == 'GET':
            for item in self.response_data:
                schedule_plan_id = item.get('schedule_plan_id')
                trigger = item.get('trigger')
                schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
                item['schedule_plan'] = schedule_plan

    def response_callback(self):
        if request.method == 'POST':
            # 创建定时计划
            data = {}
            res = current_app.test_client().post(url_for('schedule_plan.scheduleplanview'), json=data)
            # 定时计划返回数据重新
            if res.status_code == 200:
                schedule_plan_info = json.loads(res.data)
                job_id = schedule_plan_info.get('job_id')
                with db.auto_commit():
                    db.session.query(self.table_orm).filter(
                        self.table_orm.id == self.table_id).update({'job_id': job_id})
            else:
                with db.auto_commit():
                    db.session.query(self.table_orm).filter(
                        self.table_orm.id == self.table_id
                    ).update({'active': False})
                raise ValueError(f'schedule task create error::{res.data}')

        elif request.method == 'PUT':
            # 修改定时计划
            data = {}
            res = current_app.test_client().put(url_for('schedule_plan.scheduleplanview'), json=data)
            if res.status_code == 200:
                # 修改流程
                process_info = dict()
                for key, val in self.form_data.items():
                    if hasattr(Process, key):
                        process_info.setdefault(key, val)

                with db.auto_commit():
                    db.session.query(Process).filter(
                        Process.process_id == self.form_data.get('process_id')
                    ).update(process_info)
            else:
                raise ValueError(f'schedule task update error::{res.data}')

        elif request.method == 'DELETE':
            data = {}
            res = current_app.test_client().delete(url_for('schedule_plan.scheduleplanview'), json=data)
            if res.status_code != 200:
                raise ValueError(f'schedule task delete error::{res.data}')
        elif request.method == 'GET':
            self.handle_schedule_item()

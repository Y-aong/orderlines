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
from apis.orderlines.schema.schedule_task_schema import ScheduleTaskSchema, CreateScheduleTask
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
        self.origin_schedule_task = None
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

    def handle_request_params(self):
        if request.method in ['PUT', 'DELETE']:
            obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
            self.origin_schedule_task = self.table_schema().dump(obj)

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

    def get_call_back(self):
        if self.form_data.get('page') and self.form_data.get('pre_page'):
            for item in self.response_data.get('items'):
                schedule_plan_id = item.get('schedule_plan_id')
                trigger = item.get('trigger')
                schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
                item['schedule_plan'] = schedule_plan
        if self.response_data and isinstance(self.response_data, dict) and request.method == 'GET':
            trigger = self.response_data.get('trigger')
            schedule_plan_id = self.response_data.get('schedule_plan_id')
            schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
            self.response_data['schedule_plan'] = schedule_plan
        elif self.response_data and isinstance(self.response_data, list) and request.method == 'GET':
            for item in self.response_data:
                schedule_plan_id = item.get('schedule_plan_id')
                trigger = item.get('trigger')
                schedule_plan = self.get_schedule_plan(trigger, schedule_plan_id)
                item['schedule_plan'] = schedule_plan

    def post_call_bask(self):
        try:
            data = dict()
            self.form_data['job_id'] = self.form_data.get('process_id')
            for key, val in self.form_data.items():
                if key in CreateScheduleTask.model_fields:
                    data.setdefault(key, val)

            create_schedule_plan_param = CreateScheduleTask(**data)
            res = current_app.test_client().post(
                url_for('schedule_plan.scheduleplanview'),
                json=create_schedule_plan_param.model_dump()
            )
            if res.status_code == 200:
                schedule_plan_info = json.loads(res.data)
                schedule_plan_id = schedule_plan_info.get('data').get('table_id')
                with db.auto_commit():
                    db.session.query(self.table_orm).filter(
                        self.table_orm.id == self.table_id
                    ).update({'schedule_plan_id': schedule_plan_id})
            else:
                raise ValueError(res.data)
        except Exception as e:
            with db.auto_commit():
                db.session.query(self.table_orm).filter(
                    self.table_orm.id == self.table_id
                ).update({'active': False})
            raise ValueError(f'schedule task create error::{e}')

    def put_call_back(self):
        try:
            self.form_data['job_id'] = self.form_data.get('process_id')
            data = {'id': self.form_data.get('schedule_plan_id')}
            for key, val in self.form_data.items():
                if key in CreateScheduleTask.model_fields:
                    data.setdefault(key, val)
            create_schedule_plan_param = CreateScheduleTask(**data)
            res = current_app.test_client().put(url_for(
                'schedule_plan.scheduleplanview'),
                json=create_schedule_plan_param.model_dump()
            )
            if res.status_code == 200:
                # 修改流程
                process_info = {}
                for key, val in self.form_data.items():
                    if hasattr(Process, key):
                        process_info.setdefault(key, val)

                with db.auto_commit():
                    db.session.query(Process).filter(
                        Process.process_id == self.form_data.get('process_id')
                    ).update(process_info)
            else:
                raise ValueError(res.data)
        except Exception as e:
            if self.origin_schedule_task:
                with db.auto_commit():
                    db.session.query(self.table_orm).filter(
                        self.table_orm.id == self.table_id
                    ).update(self.origin_schedule_task)
            raise ValueError(f'schedule task update error::{e}')

    def delete_call_back(self):
        try:
            data = {
                "trigger": self.origin_schedule_task.get('trigger'),
                "id": self.origin_schedule_task.get('schedule_plan_id')
            }
            res = current_app.test_client().delete(url_for('schedule_plan.scheduleplanview'), json=data)
            if res.status_code != 200:
                raise ValueError(res.data)
        except Exception as e:
            with db.auto_commit():
                db.session.query(self.table_orm).filter(
                    self.table_orm.id == self.table_id
                ).update({'active': True})
            raise ValueError(f'schedule task delete error::{e}')

    def response_callback(self):
        if request.method == 'POST':
            self.post_call_bask()
        elif request.method == 'PUT':
            self.put_call_back()
        elif request.method == 'DELETE':
            self.delete_call_back()
        elif request.method == 'GET':
            self.get_call_back()

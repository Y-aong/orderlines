# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_plan_view.py
# Time       ：2023/7/7 22:07
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
import uuid

from flask import request

from apis.schedule_plan.models.schedule_plan_models import IntervalPlan, DatePlan, CrontabPlan
from apis.schedule_plan.schema.schedule_plan_schema import DatePlanSchema, IntervalPlanSchema, CrontabPlanSchema
from public.apscheduler_utils import ApschedulerUtils
from public.base_model import db
from public.base_response import generate_response
from public.base_view import BaseView


class ScheduleTaskView(BaseView):
    url = '/schedule_task'

    def __init__(self):
        super(ScheduleTaskView, self).__init__()
        self.trigger = self.form_data.get('trigger')
        self.table_orms = {
            'cron': CrontabPlan,
            'date': DatePlan,
            'interval': IntervalPlan
        }
        self.table_schemas = {
            'cron': CrontabPlanSchema,
            'date': DatePlanSchema,
            'interval': IntervalPlanSchema
        }
        self.table_orm = self.table_orms.get(self.trigger)
        self.table_schema = self.table_schemas.get(self.trigger)
        self.patrol_task_id = None
        self.task_name = None
        self.exe_type = 'schedule start'
        self.job_id = None
        self.apscheduler_utils = ApschedulerUtils()

    def get_job_id(self):
        obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
        return self.table_schema().dump(obj).get('job_id')

    def handle_request_params(self):
        if request.method == 'POST':
            self.form_data['job_id'] = str(uuid.uuid1().hex)
        if request.method == 'PUT':
            args = self.form_data.pop('args') if self.form_data.get('args') else None
            self.apscheduler_utils.modify_task(self.trigger, self.get_job_id(), args, **self.form_data)
        elif request.method == 'DELETE':
            self.apscheduler_utils.delete_task(self.get_job_id())

    def handle_response(self, data):
        if isinstance(data, dict) and request.method == 'GET':
            job_id = data.get('job_id')
            schedule_task = self.apscheduler_utils.get_task(job_id)
            self.response_data['schedule_task'] = schedule_task
        elif isinstance(data, list) and request.method == 'GET':
            for item in data:
                job_id = item.get('job_id')
                schedule_task = self.apscheduler_utils.get_task(job_id)
                item['schedule_task'] = schedule_task

    def response_callback(self):
        if request.method == 'POST':
            patrol_task_id = self.form_data.pop('patrol_task_id')
            patrol_task_name = self.form_data.pop('task_name')
            job_id = self.form_data.pop('job_id')
            self.apscheduler_utils.add_task(
                self.trigger, job_id, patrol_task_id, patrol_task_name, **self.form_data)

    def get(self):
        response_data = dict()

        if not self.form_data or self.form_data.get('pre_page'):
            for key in self.table_orms:
                self.table_orm = self.table_orms[key]
                self.table_schema = self.table_schemas[key]
                multi_data = db.session.query(self.table_orm).filter(self.table_orm.active == 1).all()
                multi_data = self.table_schema().dump(multi_data, many=True)
                self.handle_response(multi_data)
                response_data[key] = multi_data
            self.response_data = response_data
        else:
            self.handle_filter()
            self.response_data = self._get_single()
            self.handle_response(self.response_data)
        return generate_response(self.response_data)

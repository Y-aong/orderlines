# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_plan_view.py
# Time       ：2023/7/7 22:07
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    定时计划视图类
    schedule task view
"""

from flask import request

from apis.schedule_plan.models.schedule_plan_models import IntervalPlan, DatePlan, CrontabPlan
from apis.schedule_plan.schema.schedule_plan_schema import DatePlanSchema, IntervalPlanSchema, CrontabPlanSchema
from public.apscheduler_utils import ApschedulerUtils
from public.base_model import db
from public.base_view import BaseView
from public.logger import logger


class SchedulePlanView(BaseView):
    url = '/schedule_plan'

    def __init__(self):
        super(SchedulePlanView, self).__init__()
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
        self.apscheduler_utils = ApschedulerUtils()

    @property
    def process_id(self):
        process_id = self.form_data.get('process_id')

        if not process_id:
            obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
            process_id = obj.job_id
        return process_id

    def handle_request_params(self):
        if request.method in ['POST', 'PUT']:
            if self.form_data.get('schedule_plan'):
                self.form_data.update(self.form_data.get('schedule_plan'))
            self.form_data['job_id'] = self.process_id

    def handle_response_data(self):
        if request.method == 'GET':
            if isinstance(self.response_data, dict):
                job_id = self.response_data.get('job_id')
                schedule_plan = self.apscheduler_utils.get_schedule_plan(job_id)
                self.response_data['schedule_plan'] = schedule_plan
                self.response_data['enable'] = True if schedule_plan else False
            elif isinstance(self.response_data, list):
                for item in self.response_data:
                    job_id = item.get('job_id')
                    schedule_plan = self.apscheduler_utils.get_schedule_plan(job_id)
                    item['schedule_plan'] = schedule_plan
                    item['enable'] = True if schedule_plan else False

    def response_callback(self):
        if request.method == 'POST':
            try:
                self.apscheduler_utils.create_schedule_plan(
                    trigger_type=self.trigger,
                    process_id=self.process_id,
                    process_name=self.form_data.get('process_name'),
                    **self.form_data.get('schedule_plan')
                )
            except Exception as e:
                logger.error(f'create schedule task error::{e}')
                with db.auto_commit():
                    db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).delete()
        elif request.method == 'PUT':
            self.apscheduler_utils.update_schedule_plan(
                trigger_type=self.trigger,
                process_id=self.process_id,
                args=self.form_data.get('args'),
                **self.form_data.get('schedule_plan')
            )
        elif request.method == 'DELETE':
            self.apscheduler_utils.delete_schedule_plan(self.process_id)

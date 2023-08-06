# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_plan_schema.py
# Time       ：2023/7/7 22:09
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    定时计划序列化类
    Serialize classes schedule plan
"""
from marshmallow import fields


from apis.schedule_plan.models.schedule_plan_models import IntervalPlan, DatePlan, CrontabPlan, ApschedulerJobs
from public.base_schema import BaseSchema


class IntervalPlanSchema(BaseSchema):
    start_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = IntervalPlan
        exclude = ['active']


class DatePlanSchema(BaseSchema):
    run_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = DatePlan
        exclude = ['active']


class CrontabPlanSchema(BaseSchema):
    start_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = CrontabPlan
        exclude = ['active']


class ApschedulerJobsSchema(BaseSchema):
    class Meta:
        model = ApschedulerJobs

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
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.schedule_plan.models.schedule_plan_models import IntervalPlan, DatePlan, CrontabPlan, ApschedulerJobs


class IntervalPlanSchema(SQLAlchemyAutoSchema):
    start_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = IntervalPlan


class DatePlanSchema(SQLAlchemyAutoSchema):
    run_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = DatePlan


class CrontabPlanSchema(SQLAlchemyAutoSchema):
    start_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")
    end_date = fields.DateTime(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = CrontabPlan


class ApschedulerJobsSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ApschedulerJobs

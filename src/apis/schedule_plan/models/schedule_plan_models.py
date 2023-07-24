# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_plan_models.py
# Time       ：2023/7/7 21:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：Timing schedule class
"""
from public.base_model import Base, db


class IntervalPlan(Base):
    __tablename__ = 'schedule_interval_plan'

    job_id = db.Column(db.String(255), comment='task id')
    weeks = db.Column(db.Integer, comment='Interval time type-week')
    days = db.Column(db.Integer, comment='Interval time type-days')
    hours = db.Column(db.Integer, comment='Interval time type-hours')
    minutes = db.Column(db.Integer, comment='Interval time type-minutes')
    seconds = db.Column(db.Integer, comment='Interval time type-seconds')
    start_date = db.Column(db.DateTime, comment='starting point for the interval calculation')
    end_date = db.Column(db.DateTime, comment='latest possible date/time to trigger on')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='timezone')


class DatePlan(Base):
    __tablename__ = 'schedule_date_plan'

    job_id = db.Column(db.String(255), comment='task id')
    run_date = db.Column(db.DateTime, comment='Planned run time')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='timezone')


class CrontabPlan(Base):
    __tablename__ = 'schedule_crontab_plan'

    job_id = db.Column(db.String(255), comment='task id')
    year = db.Column(db.String(32), comment='A four-figure year')
    month = db.Column(db.String(32), comment='Indicates that the value range is 1-12 month')
    day = db.Column(db.String(32), comment='Indicates that the value range is 1-31 day')
    week = db.Column(db.String(32), comment='格里历2006年12月31日可以写成2006年-W52-7 扩展形式或2006W527 紧凑形式')
    day_of_week = db.Column(db.String(32), comment='Indicates the day of the week,0-6 or mon,tue,wed,thu,fri,sat,sun')
    hour = db.Column(db.String(32), comment='Indicates that the value range is 0-23')
    minute = db.Column(db.String(32), comment='Indicates that the value range is 0-59')
    second = db.Column(db.String(32), comment='Indicates that the value range is 0-59')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='timezone')
    start_date = db.Column(db.DateTime, comment='starting point for the interval calculation')
    end_date = db.Column(db.DateTime, comment='latest possible date/time to trigger on')


class ApschedulerJobs(db.Model):
    __tablename__ = 'apscheduler_jobs'

    id = db.Column(db.Unicode(191), primary_key=True)
    next_run_time = db.Column(db.Float(25), index=True)
    job_state = db.Column(db.LargeBinary, nullable=False)

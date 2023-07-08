# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : schedule_plan_models.py
# Time       ：2023/7/7 21:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：定时计划类
"""
from public.base_model import Base, db


class IntervalPlan(Base):
    __tablename__ = 'schedule_interval_plan'

    job_id = db.Column(db.String(255), comment='任务id')
    weeks = db.Column(db.Integer, comment='interval间隔时间类型-week')
    days = db.Column(db.Integer, comment='interval间隔时间类型-days')
    hours = db.Column(db.Integer, comment='interval间隔时间类型-hours')
    minutes = db.Column(db.Integer, comment='interval间隔时间类型-minutes')
    seconds = db.Column(db.Integer, comment='interval间隔时间类型-seconds')
    start_date = db.Column(db.DateTime, comment='starting point for the interval calculation')
    end_date = db.Column(db.DateTime, comment='latest possible date/time to trigger on')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='时区')


class DatePlan(Base):
    __tablename__ = 'schedule_date_plan'

    job_id = db.Column(db.String(255), comment='任务id')
    run_date = db.Column(db.DateTime, comment='计划运行时间')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='时区')


class CrontabPlan(Base):
    __tablename__ = 'schedule_crontab_plan'

    job_id = db.Column(db.String(255), comment='任务id')
    year = db.Column(db.String(32), comment='四位数的年份')
    month = db.Column(db.String(32), comment='表示取值范围为1-12月')
    day = db.Column(db.String(32), comment='表示取值范围为1-31日')
    week = db.Column(db.String(32), comment='格里历2006年12月31日可以写成2006年-W52-7 扩展形式或2006W527 紧凑形式')
    day_of_week = db.Column(db.String(32), comment='表示一周中的第几天，既可以用0-6表示也可以用其英语缩写表示,0-6 或 mon,tue,wed,thu,fri,sat,sun')
    hour = db.Column(db.String(32), comment='表示取值范围为0-23时')
    minute = db.Column(db.String(32), comment='表示取值范围为0-59分')
    second = db.Column(db.String(32), comment='表示取值范围为0-59秒')
    timezone = db.Column(db.String(64), default="Asia/Shanghai", comment='时区')
    start_date = db.Column(db.DateTime, comment='starting point for the interval calculation')
    end_date = db.Column(db.DateTime, comment='latest possible date/time to trigger on')


class ApschedulerJobs(db.Model):
    __tablename__ = 'apscheduler_jobs'

    id = db.Column(db.Unicode(191), primary_key=True)
    next_run_time = db.Column(db.Float(25), index=True)
    job_state = db.Column(db.LargeBinary, nullable=False)

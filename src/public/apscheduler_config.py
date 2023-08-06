# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : apscheduler_config.py
# Time       ：2023/7/7 21:45
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    apscheduler配置信息
    apscheduler Configuration information
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from conf.config import FlaskConfig

job_stores = {
    'default': SQLAlchemyJobStore(url=FlaskConfig.SQLALCHEMY_DATABASE_URI)
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(10)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

scheduler = BackgroundScheduler(
    jobstores=job_stores,
    executors=executors,
    job_defaults=job_defaults,
    timezone='Asia/Shanghai'
)

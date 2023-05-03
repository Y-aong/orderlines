# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : celery_config.py
# Time       ：2023/1/14 23:10
# Author     ：blue_moon
# version    ：python 3.7
# Description：celery config
"""
from datetime import timedelta

from conf.config import CeleryConfig

imports = (
    'tasks.add',
    'tasks.order_lines_run',
)

# #Timezone
enable_utc = CeleryConfig.enable_utc
timezone = CeleryConfig.timezone
beat_db_uri = CeleryConfig.beat_db_uri
# Broker and Backend
broker_url = CeleryConfig.broker_url
result_backend = CeleryConfig.broker_url
celery_config = {'beat_dburi': beat_db_uri}

beat_schedule = {
    'user_test run every 10 seconds': {
        'task': 'tasks.user_test',
        'schedule': timedelta(seconds=10),
        'args': (8, 2)
    }
}

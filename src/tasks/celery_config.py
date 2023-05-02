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

imports = (
    'tasks.add',
    'tasks.order_lines_run',
)

# #Timezone
enable_utc = False
timezone = 'Asia/Shanghai'
beat_db_uri = 'mysql+pymysql://root:123456@localhost:3306/order_lines'
# Broker and Backend
broker_url = 'redis://127.0.0.1:6379/0'
result_backend = 'redis://127.0.0.1:6379/1'
celery_config = {'beat_dburi': beat_db_uri}

beat_schedule = {
    'user_test run every 10 seconds': {
        'task': 'tasks.user_test',
        'schedule': timedelta(seconds=10),
        'args': (8, 2)
    }
}

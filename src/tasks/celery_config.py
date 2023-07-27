# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : celery_config.py
# Time       ：2023/7/8 10:40
# Author     ：Y-aong
# version    ：python 3.7
# Description：celery config
"""
from datetime import timedelta

from conf.config import CeleryConfig

imports = (
    'tasks.orderlines_run',
)

beat_schedule = {
    'test every 10 seconds': {
        'task': 'orderlines_run',
        'schedule': timedelta(seconds=10),  # 每10秒執行一次
    }
}

# #Timezone
enable_utc = CeleryConfig.enable_utc
timezone = CeleryConfig.timezone

# Broker and Backend
broker_url = CeleryConfig.broker_url
result_backend = CeleryConfig.broker_url
beat_dburi = CeleryConfig.beat_db_uri

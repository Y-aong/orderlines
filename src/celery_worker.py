# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : celery_worker.py
# Time       ：2023/7/8 10:41
# Author     ：Y-aong
# version    ：python 3.7
# Description：celery worker
"""
from apis import create_app, celery

app = create_app()
app.app_context().push()

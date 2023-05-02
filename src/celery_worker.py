# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : celery_worker.py
# Time       ：2023/1/14 23:07
# Author     ：blue_moon
# version    ：python 3.7
# Description：celery api
"""
from flask_app import create_app, celery

app = create_app()
app.app_context().push()

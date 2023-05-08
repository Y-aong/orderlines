# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : add.py
# Time       ：2023/1/14 23:10
# Author     ：blue_moon
# version    ：python 3.7
# Description：user_test, celery任务
"""
from flask_app import celery


@celery.task(name='add')
def add(x, y):
    return x + y

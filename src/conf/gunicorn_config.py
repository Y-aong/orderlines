# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : gunicorn_config.py
# Time       ：2023/7/31 16:54
# Author     ：YangYong
# version    ：python 3.10
# Description：
    gunicorn config
"""

workers = 3
worker_class = "gevent"
bind = "0.0.0.0:15900"

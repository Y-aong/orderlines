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

workers = 3  # 定义同时开启的处理请求的进程数量，根据网站流量适当调整
worker_class = "gevent"  # 采用gevent库，支持异步处理请求，提高吞吐量
bind = "0.0.0.0:15900"

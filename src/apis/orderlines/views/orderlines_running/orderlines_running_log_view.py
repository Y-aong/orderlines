# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orderlines_running_log_view.py
# Time       ：2023/8/28 15:09
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines运行时日志视图
"""
from flask import request

from flask_restful import Resource


class OrderlinesRunningLogView(Resource):
    url = '/orderlines_running_log'

    def __init__(self):
        self.form_data = request.args

    def get(self):
        return {'msg': self.form_data}

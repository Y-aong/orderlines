# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_start.py
# Time       ：2023/3/12 14:44
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import request
from flask_restful import Resource

from public.base_response import generate_response


class OrderLinesStart(Resource):
    url = '/order_lines_start'

    def __init__(self):
        self.form_data = request.json

    def post(self):
        process_id = self.form_data.get('process_id')
        from tasks.order_lines_run import order_lines_run
        order_lines_run.delay(process_id)
        return generate_response(message='流程开始运行！')

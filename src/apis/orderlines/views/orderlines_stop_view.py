# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_stop_view.py
# Time       ：2023/8/18 21:45
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    停止流程
"""
from flask import request
from flask_restful import Resource


from public.api_handle_exception import handle_api_error
from public.base_response import generate_response


class OrderlinesStopView(Resource):
    url = '/orderlines/stop'

    def __init__(self):
        self.form_data = request.json

    @handle_api_error
    def post(self):
        from orderlines import OrderLines

        process_instance_id = self.form_data.get('process_instance_id')
        stop_schedule = self.form_data.get('stop_schedule')
        OrderLines().stop_process(process_instance_id, stop_schedule)
        return generate_response(message='process begin stop')

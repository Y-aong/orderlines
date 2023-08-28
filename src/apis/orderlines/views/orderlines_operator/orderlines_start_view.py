# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_start_view.py
# Time       ：2023/3/12 14:44
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    启动流程视图
    start process view
"""
from flask import request
from flask_restful import Resource

from public.api_handle_exception import handle_api_error
from public.base_response import generate_response


class OrderLinesStartView(Resource):
    url = '/orderlines/start'

    def __init__(self):
        self.form_data = request.json

    @handle_api_error
    def post(self):
        from tasks.orderlines_run import orderlines_run

        process_id = self.form_data.get('id') or self.form_data.get('process_id')
        orderlines_run.delay(process_id=process_id)
        return generate_response(message='process begin run!')

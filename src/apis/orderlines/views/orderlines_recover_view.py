# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_recover_view.py
# Time       ：2023/8/18 22:33
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    继续流程
"""
from flask import request
from flask_restful import Resource

from public.base_response import generate_response


class OrderlinesRecoverView(Resource):
    url = '/orderlines/recover'

    def __init__(self):
        self.form_data = request.json

    def post(self):
        from orderlines import OrderLines

        process_instance_id = self.form_data.get('process_instance_id')
        recover_schedule = self.form_data.get('recover_schedule')
        OrderLines().recover_process(process_instance_id, recover_schedule)
        return generate_response(message='process begin recover')

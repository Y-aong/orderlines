# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orderlines_show_view.py
# Time       ：2023/8/28 15:02
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines大屏展示视图
"""
from flask import request

from flask_restful import Resource


class OrderlinesShowView(Resource):
    url = '/orderlines_show'

    def __init__(self):
        self.form_data = request.args

    def get(self):
        return {'data': self.form_data}

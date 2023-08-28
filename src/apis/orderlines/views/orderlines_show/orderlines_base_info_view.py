# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orderlines_base_info_view.py
# Time       ：2023/8/28 14:59
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines 基础信息首页展示
"""
from flask import request

from flask_restful import Resource


class OrderlinesBaseInfoView(Resource):
    url = '/orderlines/base_info'

    def __init__(self):
        self.form_data = request.args

    def get(self):
        return {}

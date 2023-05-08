# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_view.py
# Time       ：2023/3/12 14:56
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_restful import Resource

from flask_app.public.response import generate_response
from tasks import add


class TestView(Resource):
    url = '/test'

    def get(self):
        res = add.add.delay(12, 23)
        return generate_response({"result": res.get()})

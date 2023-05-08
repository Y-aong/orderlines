# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : response.py
# Time       ：2023/3/12 10:44
# Author     ：blue_moon
# version    ：python 3.7
# Description：自定义返回值
"""


def generate_response(data=None, message='请求成功', status_code=200):
    return {
        'message': message,
        'data': data,
        'status_code': status_code
    }

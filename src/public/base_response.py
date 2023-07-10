# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_response.py
# Time       ：2023/3/12 10:44
# Author     ：Y-aong
# version    ：python 3.7
# Description：response基类
"""

from flask import jsonify, abort


def generate_response(data=None, code=200, message='success'):
    """
    自定义响应
    :param code:状态码
    :param data:返回数据
    :param message:返回消息
    :return:
    """
    success = True if code == 200 else False
    res = jsonify(dict(code=code, success=success, data=data, message=message))
    res.status_code = 200
    return res


def generate_abort(code=401, success='failure', **kwargs, ):
    kwargs.setdefault('success', success)
    kwargs.setdefault('status_code', code)
    return abort(code, kwargs)

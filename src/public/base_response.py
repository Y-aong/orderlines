# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_response.py
# Time       ：2023/3/12 10:44
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    自定义response
    custom response
"""

from flask import jsonify, abort


def generate_response(data=None, code=200, message='success'):
    """
    自定义响应, custom response
    :param code:状态码, status_code
    :param data:返回数据, response data
    :param message:返回消息, response_message
    :return:
    """
    success = True if code == 200 else False
    res = jsonify(dict(code=code, success=success, data=data, message=message))
    res.status_code = 200
    return res


def generate_abort(code=401, success=False, **kwargs):
    kwargs.setdefault('success', success)
    kwargs.setdefault('code', code)
    return abort(code, kwargs)

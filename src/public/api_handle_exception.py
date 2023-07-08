# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : api_handle_exception.py
# Time       ：2023/7/7 21:29
# Author     ：Y-aong
# version    ：python 3.7
# Description：处理api接口的装饰器
"""

import traceback

from public.base_response import generate_response
from public.logger import logger
from flask import request


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except ValueError as e:
            logger.info(f"接口名称::{request.url},\n异常堆栈::{traceback.format_exc()}, {e}")
            return generate_response(message='客户端参数异常', code=400, data=None)
        except Exception as e:
            logger.info(f"接口名称::{request.url},\n异常堆栈::{traceback.format_exc()}, {e}")
            return generate_response(message='服务器异常', code=500, data=None)
        return res

    return wrapper
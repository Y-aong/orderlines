# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : exceptions.py
# Time       ：2023/1/15 11:37
# Author     ：blue_moon
# version    ：python 3.7
# Description：order_lines 异常类
"""


class OrderLineRunningException(Exception):
    pass


class OrderLineStopException(Exception):
    pass


class EndNodeException(Exception):
    pass


class TimeOutException(Exception):
    pass


class VariableException(Exception):
    pass


class OrderLinesRunningException(Exception):
    pass

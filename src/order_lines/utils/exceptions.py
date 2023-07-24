# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : exceptions.py
# Time       ：2023/1/15 11:37
# Author     ：Y-aong
# version    ：python 3.7
# Description：order_lines exception
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

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : db_utils.py
# Time       ：2023/2/19 21:27
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""


def get_filter(table_orm, filter_data: dict):
    filters = list()
    for key, item in filter_data.items():
        if hasattr(table_orm, key):
            _filter = getattr(table_orm, key, ) == item
            filters.append(_filter)
    return filters

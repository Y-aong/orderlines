# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_config_schema.py
# Time       ：2023/8/2 15:17
# Author     ：YangYong
# version    ：python 3.10
# Description：
    配置类序列化类
    base config schema
"""

from apis.orderlines.models.base_config import BaseConfig
from public.base_schema import BaseSchema


class BaseConfigSchema(BaseSchema):
    class Meta:
        model = BaseConfig
        exclude = ['active']

# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_config_view.py
# Time       ：2023/8/21 18:12
# Author     ：YangYong
# version    ：python 3.10
# Description：
    配置视图类
"""
from apis.config.models.base_config import BaseConfig
from apis.config.schema.base_config_schema import BaseConfigSchema
from public.base_view import BaseView


class BaseConfigView(BaseView):
    url = '/conf'

    def __init__(self):
        super(BaseConfigView, self).__init__()
        self.table_orm = BaseConfig
        self.table_schema = BaseConfigSchema

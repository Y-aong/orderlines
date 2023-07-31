# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : plugin_info_view.py
# Time       ：2023/7/23 22:40
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    插件信息视图
    Plug-in information view
"""
from apis.orderlines.models import PluginInfo
from apis.orderlines.schema.plugin_info_schema import PluginInfoSchema
from public.base_view import BaseView


class PluginInfoView(BaseView):
    url = '/plugin_info'

    def __init__(self):
        super(PluginInfoView, self).__init__()
        self.table_orm = PluginInfo
        self.table_schema = PluginInfoSchema

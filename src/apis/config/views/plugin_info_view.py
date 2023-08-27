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
from sqlalchemy import or_

from apis.config.models import PluginInfo
from apis.config.schema.plugin_info_schema import PluginInfoSchema
from public.base_view import BaseView


class PluginInfoView(BaseView):
    url = '/plugin_info'

    def __init__(self):
        super(PluginInfoView, self).__init__()
        self.table_orm = PluginInfo
        self.table_schema = PluginInfoSchema

    def handle_filter(self):
        self.filter.append(self.table_orm.active == 1)
        for key, val in self.form_data.items():
            if hasattr(self.table_orm, key) and val:
                self.filter.append(getattr(self.table_orm, key) == val)
            elif key == 'keyword' and val:
                self.filter.append(
                    or_(
                        PluginInfo.id == val,
                        PluginInfo.version == val,
                        PluginInfo.method_desc == val
                    )
                )

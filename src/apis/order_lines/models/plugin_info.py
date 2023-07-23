# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : plugin_info.py
# Time       ：2023/7/23 22:06
# Author     ：Y-aong
# version    ：python 3.7
# Description：orderlines插件信息表
"""
from public.base_model import Base, db


class PluginInfo(Base):
    __tablename__ = 'base_plugin_info'

    class_name = db.Column(db.String(64), comment='插件库类名')
    version = db.Column(db.String(64), comment='插件库版本')
    method_name = db.Column(db.String(64), comment='插件库方法名')
    method_desc = db.Column(db.String(255), comment='插件库方法描述')
    parameters = db.Column(db.JSON, comment='插件库方法参数, list类型')
    return_value = db.Column(db.JSON, comment='插件库返回值参数')

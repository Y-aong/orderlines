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

    class_name = db.Column(db.String(64), comment='Plug-in library class name')
    version = db.Column(db.String(64), comment='Plug-in library version')
    method_name = db.Column(db.String(64), comment='Plug-in library method name')
    method_desc = db.Column(db.String(255), comment='Plug-in library method desc')
    parameters = db.Column(db.JSON, comment='Plug-in library method parma, type is list')
    return_value = db.Column(db.JSON, comment='Plug-in library returns value parameters')

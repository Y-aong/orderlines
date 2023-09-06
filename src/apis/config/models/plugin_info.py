# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : plugin_info.py
# Time       ：2023/7/23 22:06
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines插件信息表
    Orderlines plug-in information table
"""
from sqlalchemy import func

from public.base_model import Base, db


class PluginInfo(Base):
    __tablename__ = 'base_plugin_info'

    class_name = db.Column(db.String(64), comment='Plug-in library class name')
    version = db.Column(db.String(64), comment='Plug-in library version')
    method_name = db.Column(db.String(64), comment='Plug-in library method name')
    method_desc = db.Column(db.String(255), comment='Plug-in library method desc')
    parameters = db.Column(db.JSON, comment='Plug-in library method parma, type is list')
    return_value = db.Column(db.JSON, comment='Plug-in library returns value parameters')
    title = db.Column(db.String(255), comment='node title')
    node_type = db.Column(db.String(255), comment='node_type')
    background = db.Column(db.String(255), default='rgb(255,255,255)', comment='node_type')
    creator_name = db.Column(db.String(64), comment='creator name')
    creator_id = db.Column(db.Integer, comment='creator id')
    updater_name = db.Column(db.String(64), comment='updater name')
    updater_id = db.Column(db.Integer, comment='updater name')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='update time')

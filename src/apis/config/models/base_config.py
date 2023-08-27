# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_config.py
# Time       ：2023/8/2 15:06
# Author     ：YangYong
# version    ：python 3.10
# Description：
    base config
    基础配置
"""
from sqlalchemy import func

from public.base_model import Base, db


class BaseConfig(Base):
    __tablename__ = 'base_config'

    config_name = db.Column(db.String(64), nullable=False, unique=True, comment='config name')
    config_value = db.Column(db.Text, nullable=False, comment='config value')
    desc = db.Column(db.String(255), comment='config value')
    insert_time = db.Column(db.DateTime, default=func.now(), comment='insert time')
    update_time = db.Column(db.DateTime, onupdate=func.now(), comment='update time')
    operator_name = db.Column(db.String(64), comment='operator name')
    operator_id = db.Column(db.String(64), comment='operator id')

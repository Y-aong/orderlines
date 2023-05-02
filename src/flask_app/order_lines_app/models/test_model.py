# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : test_model.py
# Time       ：2023/1/15 0:01
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask_app.order_lines_app.models.base_model import Base, db


class Test(Base):
    __tablename__ = 'user_test'
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, comment='数值')

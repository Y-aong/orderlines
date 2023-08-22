# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_runner.py
# Time       ：2023/1/10 22:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    模型基类
    base model
"""
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger
from sqlalchemy.pool import NullPool
from contextlib import contextmanager

from conf.config import FlaskConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


def get_filter(table_orm, filter_data: dict):
    filters = list()
    for key, item in filter_data.items():
        if hasattr(table_orm, key):
            _filter = getattr(table_orm, key, ) == item
            filters.append(_filter)
    return filters


def get_session():
    db_uri = FlaskConfig.SQLALCHEMY_DATABASE_URI
    engine = create_engine(
        url=db_uri,
        poolclass=NullPool
    )
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e


db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    id = Column(db.Integer, primary_key=True, autoincrement=True)
    active = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.active = 0

    def __getitem__(self, key):
        return getattr(self, key)

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_model.py
# Time       ：2023/1/10 22:39
# Author     ：blue_moon
# version    ：python 3.7
# Description：base model
"""
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, SmallInteger
from contextlib import contextmanager

from conf.config import FlaskConfig
from flask_app.celery_order_lines.models.db_utils import get_filter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_session():
    db_uri = FlaskConfig.SQLALCHEMY_DATABASE_URI
    engine = create_engine(db_uri)
    return sessionmaker(engine)()


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
    active = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    def delete(self):
        self.active = 0

    def __getitem__(self, key):
        return getattr(self, key)

    @staticmethod
    def insert_db(table_orm: db.Model, insert_data: dict) -> int:
        session = get_session()
        db_columns = list(insert_data.keys())
        for key in db_columns:
            if not hasattr(table_orm, key):
                insert_data.pop(key)
        instance = table_orm(**insert_data)
        session.add(instance)
        session.commit()
        return instance.id

    @staticmethod
    def update_db(table_orm: db.Model, filter_data: dict, update_dict: dict) -> int:
        session = get_session()
        filters = get_filter(table_orm, filter_data)
        instance = session.query(table_orm).filter(*filters).first()
        for key, item in update_dict.items():
            if hasattr(instance, key):
                setattr(instance, key, item)
        session.commit()
        return instance.id

    @staticmethod
    def select_db(table_orm: db.Model, filter_data: dict):
        filters = get_filter(table_orm, filter_data)
        session = get_session()
        instance = session.query(table_orm).filter(*filters).first()
        return instance if instance else None

    @staticmethod
    def delete_db(table_orm: db.Model, filter_data: dict) -> int:
        filters = get_filter(table_orm, filter_data)
        session = get_session()
        instance = session.query(table_orm).filter(*filters).first()
        instance.status = 0
        session.commit()
        return instance.id

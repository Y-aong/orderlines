# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_view.py
# Time       ：2023/3/12 13:10
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from flask import request
from flask_restful import Resource

from ..order_lines_app.models.base_model import db
from ..public.response import generate_response


class BaseView(Resource):

    def __init__(self):
        self.table_orm = None
        self.table_schema = None
        if request.method == 'GET':
            self.form_data: dict = request.args
        else:
            self.form_data: dict = request.json

        self._filter = list()
        if self.table_orm:
            self._filter.append(self.table_orm.active == 1)
        self.table_id = self.form_data.get('id')
        self.response_data = dict()

    def handle_filter(self):
        for key, value in self.form_data.items():
            if key == 'id' and value:
                self._filter.append(self.table_orm.id == value)

    def get(self):
        # 获取全部
        self.handle_filter()
        task_info = db.session.query(self.table_orm).filter(*self._filter).all()
        task_info = self.table_schema().dump(task_info, many=True)
        return generate_response(task_info)

    def post(self):
        task = self.table_schema().load(self.form_data)
        obj = self.table_orm(**task)
        db.session.add(obj)
        db.session.commit()
        self.response_data['table_id'] = obj.id
        return generate_response(message='创建成功', data=self.response_data)

    def put(self):
        obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
        info = self.table_schema().load(self.form_data)
        if not obj:
            raise ValueError(f'根据table_id:{self.table_id}找不到记录')
        db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update(info)
        db.session.commit()
        self.response_data['table_id'] = obj.id
        return generate_response(message='修改成功', data=self.response_data)

    def delete(self):
        db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update({'active': 0})
        db.session.commit()
        self.response_data['table_id'] = self.table_id
        return generate_response(message='删除成功', data=self.response_data)

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_view.py
# Time       ：2023/3/12 13:10
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    视图基类
    base view
"""
from flask import request
from flask_restful import Resource

from .api_handle_exception import handle_api_error
from .base_model import db
from .base_response import generate_response


class BaseView(Resource):

    def __init__(self):
        self.table_orm = None
        self.table_schema = None
        if request.method == 'GET' or request.method == 'DELETE':
            self.form_data: dict = request.args
        else:
            self.form_data: dict = request.json
        self.filter = list()
        self.table_id = self.form_data.get('id')
        self.response_data = dict()
        self.page = self.form_data.get('page')
        self.pre_page = self.form_data.get('pre_page')

    def handle_filter(self):
        if self.table_orm:
            self.filter.append(self.table_orm.active == 1)
        for key, value in self.form_data.items():
            if hasattr(self.table_orm, key):
                self.filter.append(getattr(self.table_orm, key) == value)

    def handle_request_params(self):
        pass

    def handle_response_data(self):
        pass

    def response_callback(self):
        pass

    def _get_single(self):
        """单条查询, Single query"""
        single_data = db.session.query(self.table_orm).filter(*self.filter).first()
        if single_data:
            return self.table_schema().dump(single_data)
        return {}

    def _get_multi(self):
        """多条查询, Multiple query"""
        multi_data = db.session.query(self.table_orm).filter(*self.filter).order_by(
            self.table_orm.id)
        if self.page and self.pre_page:
            multi_data = multi_data.paginate(page=int(self.page), per_page=int(self.pre_page))
            items = self.table_schema().dump(multi_data.items, many=True)
            total = multi_data.total
            return {'items': items, 'total': total}
        else:
            return self.table_schema().dump(multi_data, many=True)

    def check_form_data(self) -> bool:
        for key, val in self.form_data.items():
            if hasattr(self.table_orm, key):
                return False
        return True

    @handle_api_error
    def get(self):
        self.handle_filter()

        if self.check_form_data() or self.form_data.get('pre_page'):
            self.response_data = self._get_multi()
        else:
            self.response_data = self._get_single()
        self.handle_response_data()
        self.response_callback()
        return generate_response(self.response_data, message='select success')

    @handle_api_error
    def post(self):
        self.handle_request_params()
        form_data = dict()
        for key, value in self.form_data.items():
            if hasattr(self.table_orm, key):
                form_data.setdefault(key, value)
        task = self.table_schema().load(form_data)
        with db.auto_commit():
            obj = self.table_orm(**task)
            db.session.add(obj)
        self.response_data['table_id'] = obj.id
        self.table_id = obj.id
        self.handle_response_data()
        self.response_callback()
        return generate_response(message='create success', data=self.response_data)

    @handle_api_error
    def put(self):
        self.handle_request_params()
        obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
        form_data = dict()
        for key, value in self.form_data.items():
            if hasattr(self.table_orm, key):
                form_data.setdefault(key, value)
        info = self.table_schema().load(form_data)
        if not obj:
            raise ValueError(f'use table_id:{self.table_id} can not find')
        with db.auto_commit():
            db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update(info)
        self.response_data['table_id'] = obj.id
        self.handle_response_data()
        self.response_callback()
        return generate_response(message='update success', data=self.response_data)

    @handle_api_error
    def delete(self):
        self.handle_request_params()
        with db.auto_commit():
            if hasattr(self.table_orm, 'active'):
                db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update({'active': 0})
            else:
                db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).delete()

        self.response_data['table_id'] = self.table_id
        self.response_callback()
        return generate_response(message='delete success', data=self.response_data)

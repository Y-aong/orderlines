# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_view.py
# Time       ：2023/3/12 13:10
# Author     ：blue_moon
# version    ：python 3.7
# Description：flask视图基类
"""
from flask import request
from flask_restful import Resource

from conf.config import FlaskConfig
from flask_app.public.base_model import db
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
        self.page = FlaskConfig.PAGE
        self.pre_page = FlaskConfig.PRE_PAGE

    def handle_filter(self):
        for key, value in self.form_data.items():
            if getattr(self.table_orm, key):
                self._filter.append(getattr(self.table_orm, key) == value)

    def handle_request_params(self):
        """处理请求参数"""
        pass

    def handle_response_data(self):
        """处理返回值参数"""
        pass

    def response_callback(self):
        """处理response的其他后续操作"""
        pass

    def _get_single(self):
        """单条查询"""
        single_data = db.session.query(self.table_orm).filter(*self._filter).first()
        return self.table_schema().dump(single_data)

    def _get_multi(self):
        """多条查询"""
        multi_data = db.session.query(self.table_orm).filter(*self._filter).order_by(
            self.table_orm.id).paginate(page=self.page, per_page=self.pre_page)
        items = self.table_schema().dump(multi_data.items, many=True)
        total = multi_data.total
        return {'items': items, 'total': total}

    def get(self):
        # 获取全部
        self.handle_filter()
        if not self.form_data or self.form_data.get('pre_page'):
            data = self._get_multi()
        else:
            data = self._get_single()
        return generate_response(data)

    def post(self):
        self.handle_response_params()
        task = self.table_schema().load(self.form_data)
        with db.auto_commit():
            obj = self.table_orm(**task)
            db.session.add(obj)
        self.response_data['table_id'] = obj.id
        self.handle_response_data()
        self.response_callback()
        return generate_response(message='创建成功', data=self.response_data)

    def put(self):
        self.handle_response_params()
        obj = db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).first()
        info = self.table_schema().load(self.form_data)
        if not obj:
            raise ValueError(f'根据table_id:{self.table_id}找不到记录')
        with db.auto_commit():
            db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update(info)
        self.response_data['table_id'] = obj.id
        self.handle_response_data()
        self.response_callback()
        return generate_response(message='修改成功', data=self.response_data)

    def delete(self):
        self.handle_response_data()
        with db.auto_commit():
            # 设置软删除
            db.session.query(self.table_orm).filter(self.table_orm.id == self.table_id).update({'active': 0})
        self.response_data['table_id'] = self.table_id
        self.response_callback()
        return generate_response(message='删除成功', data=self.response_data)

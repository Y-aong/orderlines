# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : user_view.py
# Time       ：2023/7/9 16:28
# Author     ：Y-aong
# version    ：python 3.7
# Description：用户视图类
"""
from flask import request

from apis.system_oauth.models import SystemUser, SystemUserRoleRelation
from apis.system_oauth.schema.user_schema import SystemUserSchema
from public.base_model import db
from public.base_view import BaseView


class UserView(BaseView):
    url = '/user'

    def __init__(self):
        super(UserView, self).__init__()
        self.table_orm = SystemUser
        self.table_schema = SystemUserSchema

    def handle_response_data(self):
        role_ids = self.form_data.get('role_ids')
        if request.method in ['POST', 'PUT'] and role_ids:
            for role_id in role_ids:
                obj = SystemUserRoleRelation(user_id=self.table_id, role_id=role_id)
                db.session.add(obj)
                db.session.commit()

        elif request.method == 'DELETE':
            db.session.query(SystemUserRoleRelation).filter(SystemUserRoleRelation.user_id == self.table_id).delete()
            db.session.commit()

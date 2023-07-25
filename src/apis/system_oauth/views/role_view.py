# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : role_view.py
# Time       ：2023/7/9 16:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    角色视图
    role view
"""
from flask import request

from apis.system_oauth.models import SystemRole, SystemRolePermissionRelation
from apis.system_oauth.schema.role_schema import SystemRoleSchema
from public.base_model import db
from public.base_view import BaseView


class RoleView(BaseView):
    url = '/role'

    def __init__(self):
        super(RoleView, self).__init__()
        self.table_orm = SystemRole
        self.table_schema = SystemRoleSchema

    def handle_response_data(self):
        permission_ids = self.form_data.get('permission_ids')
        if request.method in ['POST', 'PUT'] and permission_ids:
            for permission_id in permission_ids:
                obj = SystemRolePermissionRelation(permission_id=permission_id, role_id=self.table_id)
                db.session.add(obj)
                db.session.commit()

        elif request.method == 'DELETE':
            with db.auto_commit():
                db.session.query(
                    SystemRolePermissionRelation
                ).filter(SystemRolePermissionRelation.role_id == self.table_id).delete()

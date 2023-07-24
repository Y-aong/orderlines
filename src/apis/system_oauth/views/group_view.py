# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_view.py
# Time       ：2023/7/9 16:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：group view
"""
from flask import request

from apis.system_oauth.models import SystemGroup, SystemGroupPermissionRelation
from apis.system_oauth.schema.group_schema import SystemGroupSchema
from public.base_model import db
from public.base_view import BaseView


class GroupView(BaseView):
    url = '/group'

    def __init__(self):
        super(GroupView, self).__init__()
        self.table_orm = SystemGroup
        self.table_schema = SystemGroupSchema

    def handle_response_data(self):
        permission_ids = self.form_data.get('permission_ids')
        if request.method in ['POST', 'PUT'] and permission_ids:
            for permission_id in permission_ids:
                obj = SystemGroupPermissionRelation(permission_id=permission_id, group_id=self.table_id)
                db.session.add(obj)
                db.session.commit()

        elif request.method == 'DELETE':
            with db.auto_commit():
                db.session.query(
                    SystemGroupPermissionRelation
                ).filter(SystemGroupPermissionRelation.group_id == self.table_id).delete()

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : department_view.py
# Time       ：2023/7/9 16:35
# Author     ：Y-aong
# version    ：python 3.7
# Description：部门视图
"""
from apis.system_oauth.models import SystemDepartment
from apis.system_oauth.schema.department_schema import SystemDepartmentSchema
from public.base_view import BaseView


class DepartmentView(BaseView):
    url = '/department'

    def __init__(self):
        super(DepartmentView, self).__init__()
        self.table_orm = SystemDepartment
        self.table_schema = SystemDepartmentSchema

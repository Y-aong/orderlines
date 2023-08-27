# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py.py
# Time       ：2023/7/8 15:38
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.system_oauth.views.department_view import DepartmentView
from apis.system_oauth.views.group_view import GroupView

from apis.system_oauth.views.permission_view import PermissionView
from apis.system_oauth.views.role_view import RoleView
from apis.system_oauth.views.user_view import UserView

system_oauth_blue = Blueprint("system_oauth", __name__, url_prefix="")
system_oauth_api = Api(system_oauth_blue)

system_oauth_api.add_resource(DepartmentView, DepartmentView.url)
system_oauth_api.add_resource(GroupView, GroupView.url)

system_oauth_api.add_resource(PermissionView, PermissionView.url)
system_oauth_api.add_resource(RoleView, RoleView.url)
system_oauth_api.add_resource(UserView, UserView.url)


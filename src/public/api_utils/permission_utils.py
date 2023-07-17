# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : permission_utils.py
# Time       ：2023/7/17 23:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from public.base_model import get_session
from apis.system_oauth.models import SystemPermission, SystemUser, SystemRolePermissionRelation, SystemUserRoleRelation
from apis.system_oauth.schema.user_permission_schema import SystemUserPermissionSchema


def get_user_role_permission(user_id):
    """获取用户权限"""
    session = get_session()
    permission_info = session.query(
        SystemPermission.method,
        SystemPermission.path,
        SystemPermission.name,
        SystemUser.id.label('user_id'),
        SystemUser.username.label('username')
    ).join(
        SystemUserRoleRelation, SystemUser.id == SystemUserRoleRelation.user_id
    ).join(
        SystemRolePermissionRelation, SystemUserRoleRelation.role_id == SystemRolePermissionRelation.role_id
    ).join(
        SystemPermission, SystemRolePermissionRelation.permission_id == SystemPermission.id
    ).filter(SystemUser.id == user_id).all()
    return SystemUserPermissionSchema().dump(permission_info, many=True)


def get_user_group_permission(user_id):
    """获取用户群组权限"""
    pass

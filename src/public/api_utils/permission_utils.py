# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : permission_utils.py
# Time       ：2023/7/17 23:13
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from apis.system_oauth.schema.user_schema import SystemUserSchema
from public.base_model import get_session
from apis.system_oauth.models import SystemPermission, SystemUser, SystemRolePermissionRelation, \
    SystemUserRoleRelation, SystemRole, SystemUserGroupRelation, SystemGroupPermissionRelation
from apis.system_oauth.schema.user_permission_schema import SystemUserPermissionSchema


def get_user_id_by_payload(payload: dict):
    """
    根据payload获取用户id
    @param payload:
    @return:
    """
    login_type = payload.get('login_type')
    login_value = payload.get('login_value')
    session = get_session()
    user_obj = session.query(SystemUser).filter(getattr(SystemUser, login_type) == login_value).first()
    user_info = SystemUserSchema().dump(user_obj)
    return user_info.get('id')


def get_role_by_user(user_id):
    session = get_session()
    role = session.query(
        SystemRole
    ).join(
        SystemUserRoleRelation, SystemUserRoleRelation.role_id == SystemRole.id
    ).join(
        SystemUser, SystemUserRoleRelation.user_id == SystemUser.id
    ).filter(SystemUser.id == user_id).first()

    return role.role_name if role else None


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
    session = get_session()
    permission_info = session.query(
        SystemPermission.method,
        SystemPermission.path,
        SystemPermission.name,
        SystemUser.id.label('user_id'),
        SystemUser.username.label('username')
    ).join(
        SystemUserGroupRelation, SystemUser.id == SystemUserGroupRelation.user_id
    ).join(
        SystemGroupPermissionRelation, SystemUserGroupRelation.group_id == SystemGroupPermissionRelation.group_id
    ).join(
        SystemPermission, SystemGroupPermissionRelation.permission_id == SystemPermission.id
    ).filter(SystemUser.id == user_id).all()
    return SystemUserPermissionSchema().dump(permission_info, many=True)

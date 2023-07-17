# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : role_schema.py
# Time       ：2023/7/9 16:25
# Author     ：Y-aong
# version    ：python 3.7
# Description：角色序列化类
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemRole, SystemRolePermissionRelation, SystemPermission, SystemUser, \
    SystemUserRoleRelation
from apis.system_oauth.schema.permission_schema import SystemPermissionSchema
from apis.system_oauth.schema.user_schema import SystemUserSchema
from public.base_model import get_session


def get_permission_by_role(role_id):
    permissions = list()
    session = get_session()
    objs = session.query(
        SystemRolePermissionRelation.permission_id
    ).filter(SystemRolePermissionRelation.role_id == role_id).all()

    infos = SystemRolePermissionRelationSchema().dump(objs, many=True)
    for info in infos:
        permission_id = info.get('permission_id')
        permission = session.query(SystemPermission).filter(SystemPermission.id == permission_id).first()
        permission = SystemPermissionSchema().dump(permission)
        permissions.append(permission)
    return permissions


def get_user_by_role(role_id):
    users = list()
    session = get_session()
    objs = session.query(
        SystemUserRoleRelation.user_id
    ).filter(SystemUserRoleRelation.role_id == role_id).all()

    infos = SystemUserRoleRelationSchema().dump(objs, many=True)
    for info in infos:
        user_id = info.get('user_id')
        user = session.query(SystemUser).filter(SystemUser.id == user_id).first()
        user = SystemUserSchema().dump(user)
        users.append(user)
    return users


class SystemRoleSchema(SQLAlchemyAutoSchema):
    permissions = fields.Function(serialize=lambda obj: get_permission_by_role(obj.id))
    users = fields.Function(serialize=lambda obj: get_user_by_role(obj.id))

    class Meta:
        model = SystemRole
        exclude = ['active']


class SystemRolePermissionRelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemRolePermissionRelation
        exclude = ['active']


class SystemUserRoleRelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemUserRoleRelation
        exclude = ['active']

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : group_schema.py
# Time       ：2023/7/9 16:23
# Author     ：Y-aong
# version    ：python 3.7
# Description：Group serialized class
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.system_oauth.models import SystemGroup, SystemGroupPermissionRelation, SystemPermission, \
    SystemUserGroupRelation, SystemUser
from apis.system_oauth.schema.permission_schema import SystemPermissionSchema
from apis.system_oauth.schema.user_schema import SystemUserGroupRelationSchema, SystemUserSchema
from public.base_model import get_session


def get_permission_by_group(group_id):
    permissions = list()
    session = get_session()
    objs = session.query(
        SystemGroupPermissionRelation.permission_id
    ).filter(SystemGroupPermissionRelation.group_id == group_id).all()

    infos = SystemGroupPermissionRelationSchema().dump(objs, many=True)
    for info in infos:
        permission_id = info.get('permission_id')
        permission = session.query(SystemPermission).filter(SystemPermission.id == permission_id).first()
        permission = SystemPermissionSchema().dump(permission)
        permissions.append(permission)
    return permissions


def get_user_by_group(group_id):
    users = list()
    session = get_session()
    objs = session.query(
        SystemUserGroupRelation.user_id
    ).filter(SystemUserGroupRelation.group_id == group_id).all()

    infos = SystemUserGroupRelationSchema().dump(objs, many=True)
    for info in infos:
        user_id = info.get('user_id')
        user = session.query(SystemUser).filter(SystemUser.id == user_id).first()
        user = SystemUserSchema().dump(user)
        users.append(user)
    return users


class SystemGroupSchema(SQLAlchemyAutoSchema):
    permissions = fields.Function(serialize=lambda obj: get_permission_by_group(obj.id))
    users = fields.Function(serialize=lambda obj: get_user_by_group(obj.id))

    class Meta:
        model = SystemGroup
        exclude = ['active']


class SystemGroupPermissionRelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SystemGroupPermissionRelation
        exclude = ['active']

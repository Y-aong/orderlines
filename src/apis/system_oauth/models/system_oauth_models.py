# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : system_oauth_models.py
# Time       ：2023/7/9 10:27
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    用户权限模型类
    user permission model

user——group  多对多
dept ——user 一对多
role ——permission  多对多
role ——user 多对多
group ——permission  多对多

user role  permission  group  dept
user group relation
role permission relation
group permission relation
user role relation

"""
from sqlalchemy import func

from public.base_model import Base, db
from public.api_utils.jwt_utils import encrypt_password


class SystemUser(Base):
    __tablename__ = 'system_user'

    username = db.Column(db.String(64), unique=True, comment='user name')
    email = db.Column(db.String(128), unique=True, nullable=True, comment='user email')
    phone = db.Column(db.String(128), unique=True, nullable=True, comment='user phone')
    password = db.Column(db.String(255), comment='user password')
    create_time = db.Column(db.DateTime, default=func.now(), comment='user create_time')
    user_image = db.Column(db.LargeBinary, default=b'', comment='user image')
    group_owner = db.Column(db.BOOLEAN, default=False, comment='is group owner')
    dept_id = db.Column(db.Integer, db.ForeignKey('system_department.id'), comment='dept id')

    @staticmethod
    def check_password(password, login_type, login_value):
        _password = encrypt_password(password)
        if not hasattr(SystemUser, login_type):
            raise ValueError(f'login_type::{login_type} is not exist')
        user = db.session.query(SystemUser).filter(getattr(SystemUser, login_type) == login_value).first()
        if not user:
            raise ValueError(f'user{login_value} is not exist')

        db_password = user.password
        if db_password != _password:
            raise ValueError(f'username or password error')


class SystemGroup(Base):
    __tablename__ = 'system_group'

    group_name = db.Column(db.String(128), unique=True, comment='group name')
    desc = db.Column(db.String(255), comment='group desc')
    owner_id = db.Column(db.Integer, comment='owner id')
    owner_name = db.Column(db.String(64), comment='owner name')


class SystemUserGroupRelation(Base):
    __tablename__ = 'system_user_group_relation'

    group_id = db.Column(db.Integer, comment='group id')
    user_id = db.Column(db.Integer, comment='userid')


class SystemPermission(Base):
    __tablename__ = 'system_permission'

    name = db.Column(db.String(128), comment='permission name')
    menu = db.Column(db.Boolean, default=False, comment='is menu, True: menu,False:api')
    method = db.Column(db.Enum('GET', 'POST', 'PUT', 'DELETE'), comment='method')
    path = db.Column(db.String(128), comment='Request path regular')
    # self join 
    pid = db.Column(db.Integer, comment='permission parent id')
    desc = db.Column(db.String(255), comment='permission desc')


class SystemGroupPermissionRelation(Base):
    __table_name__ = 'system_group_permission_relation'

    group_id = db.Column(db.Integer, comment='group id')
    permission_id = db.Column(db.Integer, comment='permission id')


class SystemRole(Base):
    __tablename__ = 'system_role'

    role_name = db.Column(db.String(128), comment='role name')
    desc = db.Column(db.String(255), comment='role desc')


class SystemUserRoleRelation(Base):
    __tablename__ = 'system_user_role_relation'

    user_id = db.Column(db.Integer, comment='userid')
    role_id = db.Column(db.Integer, comment='role id')


class SystemRolePermissionRelation(Base):
    __tablename__ = 'system_role_permission_relation'

    role_id = db.Column(db.Integer, comment='role id')
    permission_id = db.Column(db.Integer, comment='permission id')


class SystemDepartment(Base):
    __tablename__ = 'system_department'

    department_name = db.Column(db.String(128), comment='dept name')
    pid = db.Column(db.Integer, comment='dept parent id')
    desc = db.Column(db.String(255), comment='dept desc')
    users = db.relationship('SystemUser', backref='system_department')

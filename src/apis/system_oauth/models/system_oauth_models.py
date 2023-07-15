# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : system_oauth_models.py
# Time       ：2023/7/9 10:27
# Author     ：Y-aong
# version    ：python 3.7
# Description：用户权限模块
"""
from sqlalchemy import func

from public.base_model import Base, db
from public.api_utils.jwt_utils import encrypt_password


class SystemUser(Base):
    __tablename__ = 'system_user'

    username = db.Column(db.String(64), unique=True, comment='用户名称')
    email = db.Column(db.String(128), unique=True, nullable=True, comment='用户邮箱')
    phone = db.Column(db.String(128), unique=True, nullable=True, comment='用户电话')
    password = db.Column(db.String(255), comment='用户密码')
    create_time = db.Column(db.DateTime, default=func.now(), comment='用户创建时间')
    user_image = db.Column(db.LargeBinary, default=b'', comment='用户头像')
    group_owner = db.Column(db.BOOLEAN, default=False, comment='是否为群组owner')

    @staticmethod
    def check_password(password, login_type, login_value):
        _password = encrypt_password(password)
        if not hasattr(SystemUser, login_type):
            raise ValueError(f'当前没有{login_type}登录方式')
        user = db.session.query(SystemUser).filter(getattr(SystemUser, login_type) == login_value).first()
        if not user:
            raise ValueError(f'用户{login_value}不存在')

        db_password = user.password
        if db_password != _password:
            raise ValueError(f'用户名或者密码错误')

    def get_all_permission(self):
        """获取用户的所有权限"""
        pass


class SystemGroup(Base):
    __tablename__ = 'system_group'
    group_name = db.Column(db.String(128), unique=True, comment='群组名称')
    desc = db.Column(db.String(255), comment='群组描述')
    # 群主owner
    owner_id = db.Column(db.Integer, comment='群主id')
    owner_name = db.Column(db.String(64), comment='群主名称')


class SystemGroupPermissionRelation(Base):
    __table_name__ = 'system_group_permission_relation'
    group_id = db.Column(db.Integer, comment='群组id')
    permissions_id = db.Column(db.Integer, comment='权限id')


class SystemUserGroupRelation(Base):
    __tablename__ = 'system_user_group_relation'
    group_id = db.Column(db.Integer, comment='群组id')
    user_id = db.Column(db.Integer, comment='用户id')


class SystemPermission(Base):
    __tablename__ = 'system_permission'
    name = db.Column(db.String(128), comment='权限名')
    sign = db.Column(db.String(128), unique=True, comment='权限标识')
    menu = db.Column(db.Boolean, comment='是否为菜单, True为菜单,False为接口')
    method = db.Column(db.Enum('GET, POST, PUT, DELETE'), comment='方法')
    path = db.Column(db.String(128), comment='请求路径正则')
    # 自关联
    pid = db.Column(db.Integer, comment='权限父id')
    desc = db.Column(db.String(255), comment='权限描述')


class SystemRole(Base):
    __tablename__ = 'system_role'
    role_name = db.Column(db.String(128), comment='角色名')
    desc = db.Column(db.String(255), comment='角色描述')


class SystemUserRoleRelation(Base):
    __tablename__ = 'system_user_role_relation'
    role_id = db.Column(db.Integer, comment='权限id')
    user_id = db.Column(db.Integer, comment='用户id')


class SystemDepartment(Base):
    __tablename__ = 'system_department'
    department_name = db.Column(db.String(128), comment='部门名称')
    pid = db.Column(db.Integer, comment='部门父id')
    desc = db.Column(db.String(255), comment='部门描述')


class SystemDeptUserRelation(Base):
    __tablename__ = 'system_dept_user_relation'

    dept_id = db.Column(db.Integer, comment='部门id')
    user_id = db.Column(db.Integer, comment='用户id')

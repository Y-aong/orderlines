# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : teacher_student_model.py
# Time       ：2023/7/16 10:42
# Author     ：Y-aong
# version    ：python 3.7
# Description：sqlalchemy一对多，一对一，多对多关系配置
"""
from public.base_model import db, Base


# 配置一对多关系
class Student(Base):
    __tablename__ = 'student'

    name = db.Column(db.String(64), comment='学生名称')
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    # 方式二
    # teacher = db.relationship("Teacher", back_populates="student")


class Teacher(Base):
    __tablename__ = 'teacher'
    name = db.Column(db.String(64), comment='教师名称')
    # 方式一、backref，要在一对多中建立双向关系，“反向”端是多对一，
    student = db.relationship('Student', backref='teacher')
    # 方式二、back_populates
    # student = db.relationship('Student', back_populates='student')

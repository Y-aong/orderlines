# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : teacher_student_schema.py
# Time       ：2023/7/16 21:41
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from apis.test.models import Teacher, Student

from public.base_model import get_session


def get_teacher(obj):
    session = get_session()
    teacher_obj = session.query(Teacher).filter(Teacher.id == obj.teacher_id).first()
    return TeacherStudentSchema().dump(teacher_obj)


class StudentSchema(SQLAlchemyAutoSchema):
    teacher = fields.Function(serialize=lambda obj: get_teacher(obj))

    class Meta:
        model = Student
        exclude = ['active']


class TeacherSchema(SQLAlchemyAutoSchema):
    student = fields.Nested(StudentSchema, many=True, dump_only=True, only=('id', 'name'))

    class Meta:
        model = Teacher


class TeacherStudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        fields = ["id", "name"]

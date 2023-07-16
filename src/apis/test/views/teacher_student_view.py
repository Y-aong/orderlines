# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : teacher_student_view.py
# Time       ：2023/7/16 11:02
# Author     ：Y-aong
# version    ：python 3.7
# Description：一对多视图
"""
from apis.test.models.teacher_student_model import Teacher, Student
from apis.test.schemas.teacher_student_schema import TeacherSchema, StudentSchema
from public.base_view import BaseView


class TeacherView(BaseView):
    url = '/teacher'

    def __init__(self):
        super(TeacherView, self).__init__()
        self.table_orm = Teacher
        self.table_schema = TeacherSchema


class StudentView(BaseView):
    url = '/student'

    def __init__(self):
        super(StudentView, self).__init__()
        self.table_orm = Student
        self.table_schema = StudentSchema

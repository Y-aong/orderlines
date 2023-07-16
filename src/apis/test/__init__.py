# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py.py
# Time       ：2023/7/16 10:41
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.test.views.teacher_student_view import StudentView, TeacherView

test_blue = Blueprint("test", __name__, url_prefix="")
test_api = Api(test_blue)

test_api.add_resource(TeacherView, TeacherView.url)
test_api.add_resource(StudentView, StudentView.url)


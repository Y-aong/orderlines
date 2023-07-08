# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py.py
# Time       ：2023/7/7 21:22
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.schedule_plan.views.schedule_plan_view import ScheduleTaskView

schedule_plan_blue = Blueprint("schedule_task", __name__, url_prefix="")
schedule_task_api = Api(schedule_plan_blue)

schedule_task_api.add_resource(ScheduleTaskView, ScheduleTaskView.url)

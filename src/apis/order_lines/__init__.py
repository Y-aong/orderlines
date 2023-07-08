# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py.py
# Time       ：2023/3/11 17:52
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.order_lines.views import (
    TaskView, TaskInstanceView, ProcessView, ProcessInstanceView, OrderLinesBuildView, OrderLinesStart)

order_line_blue = Blueprint("order_line", __name__, url_prefix="")
schedule_task_api = Api(order_line_blue)

schedule_task_api.add_resource(TaskView, TaskView.url)
schedule_task_api.add_resource(TaskInstanceView, TaskInstanceView.url)
schedule_task_api.add_resource(ProcessView, ProcessView.url)
schedule_task_api.add_resource(ProcessInstanceView, ProcessInstanceView.url)
schedule_task_api.add_resource(OrderLinesBuildView, OrderLinesBuildView.url)
schedule_task_api.add_resource(OrderLinesStart, OrderLinesStart.url)

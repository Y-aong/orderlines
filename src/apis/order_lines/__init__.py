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

from apis.order_lines.views import TaskView, TaskInstanceView, ProcessView, ProcessInstanceView, OrderLinesBuildView
from apis.order_lines.views.order_lines_start_view import OrderLinesStartView
from apis.order_lines.views.plugin_info_view import PluginInfoView

order_line_blue = Blueprint("order_line", __name__, url_prefix="")
order_line_api = Api(order_line_blue)

order_line_api.add_resource(TaskView, TaskView.url)
order_line_api.add_resource(TaskInstanceView, TaskInstanceView.url)
order_line_api.add_resource(ProcessView, ProcessView.url)
order_line_api.add_resource(ProcessInstanceView, ProcessInstanceView.url)
order_line_api.add_resource(OrderLinesBuildView, OrderLinesBuildView.url)
order_line_api.add_resource(OrderLinesStartView, OrderLinesStartView.url)
order_line_api.add_resource(PluginInfoView, PluginInfoView.url)

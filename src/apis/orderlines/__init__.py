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

from apis.orderlines.views import TaskView, TaskInstanceView, ProcessView, ProcessInstanceView
from apis.orderlines.views.orderlines_build_view import ProcessBuildView
from apis.orderlines.views.orderlines_recover_view import OrderlinesRecoverView
from apis.orderlines.views.orderlines_paused_view import OrderlinesPausedView
from apis.orderlines.views.orderlines_start_view import OrderLinesStartView
from apis.orderlines.views.orderlines_stop_view import OrderlinesStopView
from apis.config.views.plugin_info_view import PluginInfoView
from apis.orderlines.views.process_instance_view import ProcessInstanceReportView, ProcessInstanceExcelReportView, \
    ProcessInstanceHtmlReportView
from apis.orderlines.views.schedule_task_view import ScheduleTaskView

order_line_blue = Blueprint("order_line", __name__, url_prefix="")
order_line_api = Api(order_line_blue)

order_line_api.add_resource(TaskView, TaskView.url)
order_line_api.add_resource(TaskInstanceView, TaskInstanceView.url)
order_line_api.add_resource(ProcessView, ProcessView.url)
order_line_api.add_resource(ProcessInstanceView, ProcessInstanceView.url)
order_line_api.add_resource(ProcessBuildView, ProcessBuildView.url)
order_line_api.add_resource(OrderLinesStartView, OrderLinesStartView.url)
order_line_api.add_resource(OrderlinesStopView, OrderlinesStopView.url)
order_line_api.add_resource(OrderlinesPausedView, OrderlinesPausedView.url)
order_line_api.add_resource(OrderlinesRecoverView, OrderlinesRecoverView.url)
order_line_api.add_resource(ProcessInstanceReportView, ProcessInstanceReportView.url)
order_line_api.add_resource(ProcessInstanceExcelReportView, ProcessInstanceExcelReportView.url)
order_line_api.add_resource(ProcessInstanceHtmlReportView, ProcessInstanceHtmlReportView.url)
order_line_api.add_resource(ScheduleTaskView, ScheduleTaskView.url)

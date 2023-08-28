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

from apis.orderlines.views import TaskView, TaskInstanceView
from apis.orderlines.views.orderlines_build.orderlines_build_view import ProcessBuildView
from apis.orderlines.views.orderlines_manager.process_view import ProcessView
from apis.orderlines.views.orderlines_operator.orderlines_recover_view import OrderlinesRecoverView
from apis.orderlines.views.orderlines_operator.orderlines_paused_view import OrderlinesPausedView
from apis.orderlines.views.orderlines_operator.orderlines_start_view import OrderLinesStartView
from apis.orderlines.views.orderlines_operator.orderlines_stop_view import OrderlinesStopView
from apis.orderlines.views.orderlines_manager.process_instance_view import ProcessInstanceReportView, \
    ProcessInstanceExcelReportView, ProcessInstanceView
from apis.orderlines.views.orderlines_running.orderlines_running_log_view import OrderlinesRunningLogView
from apis.orderlines.views.orderlines_schedule.schedule_task_view import ScheduleTaskView
from apis.orderlines.views.orderlines_show.orderlines_base_info_view import OrderlinesBaseInfoView
from apis.orderlines.views.orderlines_show.orderlines_export_view import ProcessInstanceHtmlReportView
from apis.orderlines.views.orderlines_show.orderlines_show_view import OrderlinesShowView

orderlines_blue = Blueprint("orderlines", __name__, url_prefix="")
orderlines_api = Api(orderlines_blue)

orderlines_api.add_resource(TaskView, TaskView.url)
orderlines_api.add_resource(TaskInstanceView, TaskInstanceView.url)
orderlines_api.add_resource(ProcessView, ProcessView.url)
orderlines_api.add_resource(ProcessInstanceView, ProcessInstanceView.url)
orderlines_api.add_resource(ProcessBuildView, ProcessBuildView.url)
orderlines_api.add_resource(OrderLinesStartView, OrderLinesStartView.url)
orderlines_api.add_resource(OrderlinesStopView, OrderlinesStopView.url)
orderlines_api.add_resource(OrderlinesPausedView, OrderlinesPausedView.url)
orderlines_api.add_resource(OrderlinesRecoverView, OrderlinesRecoverView.url)
orderlines_api.add_resource(ProcessInstanceReportView, ProcessInstanceReportView.url)
orderlines_api.add_resource(ProcessInstanceExcelReportView, ProcessInstanceExcelReportView.url)
orderlines_api.add_resource(ProcessInstanceHtmlReportView, ProcessInstanceHtmlReportView.url)
orderlines_api.add_resource(ScheduleTaskView, ScheduleTaskView.url)
orderlines_api.add_resource(OrderlinesRunningLogView, OrderlinesRunningLogView.url)
orderlines_api.add_resource(OrderlinesBaseInfoView, OrderlinesBaseInfoView.url)
orderlines_api.add_resource(OrderlinesShowView, OrderlinesShowView.url)

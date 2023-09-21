# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py.py
# Time       ：2023/9/14 9:28
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.flow.views.flow_data_view import FlowDataView
from apis.flow.views.flow_save_view import FlowSaveView
from apis.flow.views.flow_task_config_view import FlowTaskConfigView
from apis.flow.views.menu_node_view import NodeMenuView
from apis.flow.views.prev_node_result_view import PrevNodeResultView
from apis.flow.views.process_control_view import ProcessControlView
from apis.flow.views.task_node_view import TaskNodeView

flow_blue = Blueprint("flow", __name__, url_prefix="")
flow_api = Api(flow_blue)
flow_api.add_resource(NodeMenuView, NodeMenuView.url)
flow_api.add_resource(TaskNodeView, TaskNodeView.url)
flow_api.add_resource(FlowTaskConfigView, FlowTaskConfigView.url)
flow_api.add_resource(FlowDataView, FlowDataView.url)
flow_api.add_resource(FlowSaveView, FlowSaveView.url)
flow_api.add_resource(ProcessControlView, ProcessControlView.url)
flow_api.add_resource(PrevNodeResultView, PrevNodeResultView.url)

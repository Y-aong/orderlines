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

from apis.flow.views.plugin_node_view import NodeMenuView
from apis.flow.views.task_node_view import TaskNodeView

flow_blue = Blueprint("flow", __name__, url_prefix="")
flow_api = Api(flow_blue)
flow_api.add_resource(NodeMenuView, NodeMenuView.url)
flow_api.add_resource(TaskNodeView, TaskNodeView.url)

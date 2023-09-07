# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : __init__.py.py
# Time       ：2023/8/21 18:11
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.config.views.base_config_view import BaseConfigView
from apis.config.views.default_task_config_view import DefaultTaskConfigView
from apis.config.views.plugin_info_view import PluginInfoView
from apis.config.views.plugin_node_view import PluginNodeView
from apis.config.views.plugin_param_result_view import PluginParamResultView

conf_blue = Blueprint("conf", __name__, url_prefix="")
conf_api = Api(conf_blue)
conf_api.add_resource(PluginInfoView, PluginInfoView.url)
conf_api.add_resource(BaseConfigView, BaseConfigView.url)
conf_api.add_resource(PluginNodeView, PluginNodeView.url)
conf_api.add_resource(PluginParamResultView, PluginParamResultView.url)
conf_api.add_resource(DefaultTaskConfigView, DefaultTaskConfigView.url)

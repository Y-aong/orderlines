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
from apis.config.views.plugin_info_view import PluginInfoView

conf_blue = Blueprint("conf", __name__, url_prefix="")
conf_api = Api(conf_blue)
conf_api.add_resource(PluginInfoView, PluginInfoView.url)
conf_api.add_resource(BaseConfigView, BaseConfigView.url)

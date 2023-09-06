# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : plugin_param_result_view.py
# Time       ：2023/9/6 17:45
# Author     ：YangYong
# version    ：python 3.10
# Description：
    获取插件的参数和返回值
"""
from flask import request
from flask_restful import Resource

from apis.config.models import PluginInfo
from apis.config.schema.plugin_info_schema import PluginInfoParamSchema
from public.base_model import db
from public.base_response import generate_response


class PluginParamResultView(Resource):
    url = '/plugin_param_result'

    def __init__(self):
        self.form_data = request.args

    def get(self):
        obj = db.session.query(PluginInfo).filter(
            PluginInfo.method_name == self.form_data.get('method_name'),
            PluginInfo.class_name == self.form_data.get('class_name'),
            PluginInfo.version == self.form_data.get('version')
        ).first()
        plugin_info = PluginInfoParamSchema().dump(obj)
        return generate_response(plugin_info)

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_build_view.py
# Time       ：2023/3/12 13:22
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    创建流程视图
    build process view
"""

from flask import request

from flask_restful import Resource

from orderlines.process_build.process_build_adapter import ProcessBuildAdapter
from public.api_handle_exception import handle_api_error
from public.base_response import generate_response


class ProcessBuildView(Resource):
    url = '/process/build'

    def __init__(self):
        self.form_data: dict = request.json
        self.build_type = None
        self.process_build = ProcessBuildAdapter()
        self.build_types = {
            'json': self.process_build.build_by_json,
            'yaml': self.process_build.build_by_yaml,
            'dict': self.process_build.build_by_dict,
        }

    @handle_api_error
    def post(self):
        if not self.form_data.get('build_type'):
            raise ValueError('build type must required')
        self.build_type = self.form_data.pop('build_type')
        table_id = self.build_types.get(self.build_type)(**self.form_data)
        return generate_response({'id': table_id}, message='process build success')

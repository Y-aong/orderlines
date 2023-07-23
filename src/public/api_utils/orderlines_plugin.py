# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_plugin.py
# Time       ：2023/7/20 21:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：orderlines插件库插件，自动将插件中的函数信息写到数据库中
"""
import inspect
import json
from typing import Any

from pydantic import BaseModel

from order_lines.running.module_check import CheckModule

from public.logger import logger


class OrderlinesPlugHelper:

    def __init__(self):
        self.base_params = ['process_info']

    def init_plugin(self):
        plugins = list()
        modules = CheckModule().get_module()
        for key in modules.values():
            plugin = self.handle_orderlines_plugin(key)
            plugins.append(plugin)
        logger.info(json.dumps(plugins))

    def parse_pydantic_params(self, params: BaseModel):
        """解析pydantic类型的注解"""
        field_infos = list()
        properties = params.model_json_schema().get('properties')
        model_fields = params.model_fields
        for property_name, property_val in properties.items():
            if property_name not in self.base_params:
                field_infos.append({
                    'name': property_name,
                    'title': property_val.get('title'),
                    'type': str(model_fields.get(property_name).annotation),
                    'default': property_val.get('default'),
                    'required': False if property_val.get('default') else True,
                    'desc': property_val.get('description'),
                })

        return field_infos

    @staticmethod
    def parse_common_params(params: Any):
        field_infos = list()
        for name, param in dict(params).items():
            if name != 'self':
                field_infos.append({
                    'name': str(param.name),
                    'annotation': '' if "empty" in str(param.annotation) else str(param.annotation),
                    'default': '' if "empty" in str(param.default) else str(param.default),
                    'desc': ''
                })
        return field_infos

    @staticmethod
    def handle_func_doc(func_doc: str) -> str:
        """处理函数的注释"""

        if not func_doc:
            return ''

        func_doc = func_doc.replace('  ', '')
        if '\n' in func_doc:
            return func_doc.split('\n')[1]
        else:
            return func_doc

    def get_func_info(self, model, attr_name):
        parameters_info = []
        sig = inspect.signature(getattr(model, attr_name))
        parameters = sig.parameters
        return_annotation = sig.return_annotation
        arg_keys = tuple(arg for arg in parameters.keys() if arg != 'self')
        for arg_name in arg_keys:
            try:
                parameters_info = self.parse_pydantic_params(parameters[arg_name].annotation)
            except AttributeError:
                parameters_info = self.parse_common_params(parameters)

        try:
            return_annotation = self.parse_pydantic_params(return_annotation)
        except AttributeError:
            annotation = '' if "empty" in repr(return_annotation) else str(return_annotation)
            return_annotation = {'name': '', 'annotation': annotation, 'desc': '', 'default': ''}
        func_doc = getattr(model, attr_name).__doc__
        return parameters_info, return_annotation, self.handle_func_doc(func_doc)

    def handle_orderlines_plugin(self, model):
        class_info = dict()
        methods = list()
        for attr in dir(model):
            if not attr.startswith('_') and callable(getattr(model, attr)):
                parameters_info, return_annotation, func_doc = self.get_func_info(model, attr)
                methods.append({
                    'method_name': attr,
                    'method_desc': func_doc,
                    'parameters': parameters_info,
                    'return': return_annotation,
                })
                if methods:
                    class_info['class_name'] = model.__name__
                    class_info['methods'] = methods
                if hasattr(model, 'version'):
                    class_info['version'] = getattr(model, 'version')

        return class_info

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
from pydantic_core import PydanticUndefined

from order_lines.running.module_check import CheckModule
from public.logger import logger


class OrderlinesPlugHelper:

    def init_plugin(self):
        plugins = list()
        modules = CheckModule().get_module()
        for key in modules.values():
            plugin = self.handle_orderlines_plugin(key)
            plugins.append(plugin)
        logger.info(json.dumps(plugins))

    @staticmethod
    def parse_pydantic_params(params: BaseModel):
        """解析pydantic类型的注解"""
        field_infos = list()

        for field_name, field_info in params.model_fields.items():
            field_infos.append({
                'name': field_name,
                'annotation': str(field_info.annotation),
                'desc': '',
                'default': None if field_info.default is PydanticUndefined else field_info.default
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

    def get_func_info(self, model, attr_name):
        parameters_info = []
        sig = inspect.signature(getattr(model, attr_name))
        parameters = sig.parameters  # 参数有序字典
        return_annotation = sig.return_annotation  # 参数有序字典
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

        return parameters_info, return_annotation

    def handle_orderlines_plugin(self, model):
        plugin = list()
        for attr in dir(model):
            data = dict()
            if not attr.startswith('_') and callable(getattr(model, attr)):
                parameters_info, return_annotation = self.get_func_info(model, attr)
                data['parameters_info'] = parameters_info
                data['return_annotation'] = return_annotation
                data['class_name'] = model.__name__
                if hasattr(model, 'version'):
                    data['version'] = getattr(model, 'version')
            if data:
                plugin.append(data)

        return plugin

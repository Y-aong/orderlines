# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : orderlines_plugin.py
# Time       ：2023/7/20 21:53
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines插件工具，自动将插件中的函数信息写到数据库中
    The plug-in tool automatically writes the function information in the plug-in to the database
"""
import inspect
from typing import Any

from pydantic import BaseModel

from apis.config.models.plugin_info import PluginInfo
from orderlines.task_running.running_check import CheckModule
from public.base_model import get_session


class OrderlinesPlugHelper:

    def __init__(self):
        self.session = get_session()
        self.base_params = ['process_id', 'process_name', 'process_info',
                            'task_nodes', 'task_id', 'task_config', 'result', 'process_instance_id']
        self.exclude_method = ['on_receive', 'on_success', 'on_failure']

    def init_plugin(self):
        modules = CheckModule().get_module()
        for key in modules.values():
            plugin = self.handle_orderlines_plugin(key)
            self.insert_info_plugin_info(plugin)

    def insert_info_plugin_info(self, plugin):

        methods = plugin.get('methods')
        for method in methods:
            obj = self.session.query(PluginInfo).filter(
                PluginInfo.class_name == plugin.get('class_name'),
                PluginInfo.version == plugin.get('version'),
                PluginInfo.method_name == method.get('method_name')).first()
            plugin_info = {
                'class_name': plugin.get('class_name'),
                'version': plugin.get('version'),
                'method_name': method.get('method_name'),
                'method_desc': method.get('method_desc'),
                'parameters': method.get('parameters'),
                'return_value': method.get('return'),
            }
            if obj:
                self.session.query(PluginInfo).filter(
                    PluginInfo.class_name == plugin.get('class_name'),
                    PluginInfo.version == plugin.get('version'),
                    PluginInfo.method_name == method.get('method_name')).update(plugin_info)
                self.session.commit()
            else:
                obj = PluginInfo(**plugin_info)
                self.session.add(obj)
                self.session.commit()

    def parse_pydantic_annotation(self, annotation: BaseModel, is_params=True):
        """解析pydantic类型的注解,Parse annotations of type pydantic"""
        field_infos = list()
        properties = annotation.model_json_schema().get('properties')
        model_fields = annotation.model_fields
        for property_name, property_val in properties.items():
            annotation_info = {
                'name': property_name,
                'title': property_val.get('title'),
                'type': str(model_fields.get(property_name).annotation),
                'default': property_val.get('default'),
                'required': False if property_val.get('default') else True,
                'desc': property_val.get('description'),
            }
            if property_name not in self.base_params and is_params:
                field_infos.append(annotation_info)
            if not is_params:
                field_infos.append(annotation_info)

        return field_infos

    @staticmethod
    def parse_common_annotation(params: Any):
        field_infos = list()
        for name, param in dict(params).items():
            if name != 'self':
                default = '' if "empty" in str(param.default) else str(param.default)
                field_infos.append({
                    'name': str(param.name),
                    'title': str(param.name).title(),
                    'type': '' if "empty" in str(param.annotation) else str(param.annotation),
                    'default': default,
                    'required': False if default else True,
                    'desc': ''
                })
        return field_infos

    @staticmethod
    def handle_func_doc(func_doc: str) -> str:
        """处理函数的注释, Handles comments of functions"""
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
                parameters_info = self.parse_pydantic_annotation(parameters[arg_name].annotation, True)
            except AttributeError:
                parameters_info = self.parse_common_annotation(parameters)

        try:
            return_annotation = self.parse_pydantic_annotation(return_annotation, False)
        except AttributeError:
            annotation = '' if "empty" in repr(return_annotation) else str(return_annotation)
            return_annotation = [{
                'name': '', 'title': '', 'type': annotation,
                'default': '', 'required': True, 'desc': ''
            }]
        func_doc = getattr(model, attr_name).__doc__
        return parameters_info, return_annotation, self.handle_func_doc(func_doc)

    def handle_orderlines_plugin(self, model):
        class_info = dict()
        methods = list()
        for attr in dir(model):
            if not attr.startswith('_') and callable(getattr(model, attr)) and attr not in self.exclude_method:
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

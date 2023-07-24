# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : module_check.py
# Time       ：2023/1/16 20:27
# Author     ：Y-aong
# version    ：python 3.7
# Description：运行时检查模块是否存在
"""
import importlib
import inspect
from conf.config import OrderLinesConfig as Config
from order_lines.libraries import STANDARD_LIBS


def dynamic_import(module_name: str, class_name):
    """
    动态导入组件库，这里类名必须要和模块名一致
    Import component libraries dynamically, where the class name must match the module name
    :param module_name: 模块名，参考配置文件中的标准库.Module name, refer to the standard library in the configuration file
    :param class_name: 类名元组.Class name tuple
    :return:
    """
    modules = dict()
    for _class in class_name:
        module_str = f'{module_name}.{_class}'
        module = importlib.import_module(module_str)
        for name, sub in inspect.getmembers(module, inspect.isclass):
            if modules.get(name):
                raise ValueError(f'The same name {name} already exists')
            if sub.__base__.__name__ == 'BaseTask':
                modules[name] = sub
    return modules


class CheckModule:
    def __init__(self):
        self.modules = dict()
        self.task_module_locations = Config.std_lib_location
        self.class_name = STANDARD_LIBS

    def get_module(self):
        for task_module_location in self.task_module_locations:
            modules = dynamic_import(task_module_location, self.class_name)
            self.modules.update(modules)
        return self.modules

    def check_module(self, module_name: str):
        self.get_module()
        if not self.modules.get(module_name):
            raise AttributeError(f'module name {module_name} not find, {self.modules}')

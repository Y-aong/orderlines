# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_operator.py
# Time       ：2023/2/22 22:28
# Author     ：Y-aong
# version    ：python 3.7
# Description：变量处理
"""
from typing import Any

from orderlines.variable.variable_match import VariableMatch


class VariableOperator:
    def __init__(self, variable_config_value: str, real_variable_value: Any, variable_type: str):
        """
        变量运算. Variable operation
        :param variable_config_value: 在任务节点的配置中variable_value的key
        "result": [
            {
                "variable_key": variable_value,
                "variable_type": "int",
                "variable_desc": "subtraction函数的返回值"
            }
        ],
        流程中配置的变量名如${value}, ${add_value}+1
        The variable name configured in the process is ${value}, ${add_value}+1
        :param real_variable_value: 对应数据库中add_value的值,The value corresponding to add value in the database
        :param variable_type: 对应数据库中变量的类型,Indicates the type is a variable in the database
        """

        self.variable_config_value = variable_config_value
        self.real_variable_value = real_variable_value
        self.variable_type = variable_type
        self.variable_name = VariableMatch(self.variable_config_value).get_variable_name()

    def variable_operator(self):
        """
        变量的运算. variable operator
        :return:真正的变量值供流程使用，The real variable values are used by the process
        """
        match = '${' + self.variable_name + "}"
        return self._variable_handler(match)

    def _variable_handler(self, match):
        """变量处理方法"""
        if self.variable_type == 'str' and '+' in self.variable_config_value:
            self.variable_config_value = self.variable_config_value.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_config_value.split('+')
            return f"{v1}{v2}"
        elif self.variable_type == 'int' and '+' in self.variable_config_value:
            self.variable_config_value = self.variable_config_value.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_config_value.split('+')
            return int(v1) + int(v2)
        elif self.variable_type == 'int' and '-' in self.variable_config_value:
            self.variable_config_value = self.variable_config_value.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_config_value.split('-')
            return int(v1) - int(v2)
        elif self.variable_type == 'int' and '*' in self.variable_config_value:
            self.variable_config_value = self.variable_config_value.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_config_value.split('*')
            return int(v1) * int(v2)
        elif self.variable_type == 'int' and '/' in self.variable_config_value:
            self.variable_config_value = self.variable_config_value.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_config_value.split('/')
            return int(v1) / int(v2)
        else:
            return self.real_variable_value

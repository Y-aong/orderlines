# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : variable_operator.py
# Time       ：2023/2/22 22:28
# Author     ：Y-aong
# version    ：python 3.7
# Description：变量处理
"""
from orderlines.variable.match import Match


class VariableOperator:
    def __init__(self, variable_key, real_variable_value, variable_type):
        """
        变量运算. Variable operation
        :param variable_key:  "result": [
            {
                "variable_key": variable_value,
                "variable_type": "int",
                "variable_desc": "subtraction函数的返回值"
            }
        ],
        流程中配置的变量名如${value}, ${add_value}+1
        The variable name configured in the process is ${value}, ${add_value}+1
        :param real_variable_value: 对应数据库中add_value的值,The value corresponding to add value in the database
        :param variable_type: 对应数据库中变量的类型,Indicates the type of a variable in the database
        """

        self.variable_key = variable_key
        self.real_variable_value = real_variable_value
        self.variable_type = variable_type
        self.variable_name = Match(self.variable_key).get_variable_name()

    def variable_operator(self):
        """
        变量的运算. variable operator
        :return:真正的变量值供流程使用，The real variable values are used by the process
        """
        match = '${' + self.variable_name + "}"
        variable_value = self._variable_handler(match)
        return variable_value

    def _variable_handler(self, match):
        """变量处理方法"""
        if self.variable_type == 'str' and '+' in self.variable_key:
            self.variable_key = self.variable_key.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_key.split('+')
            return f"{v1, v2}"
        elif self.variable_type == 'int' and '+' in self.variable_key:
            self.variable_key = self.variable_key.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_key.split('+')
            return int(v1) + int(v2)
        elif self.variable_type == 'float' and '-' in self.variable_key:
            self.variable_key = self.variable_key.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_key.split('-')
            return float(v1) - float(v2)
        elif self.variable_type == 'int' and '*' in self.variable_key:
            self.variable_key = self.variable_key.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_key.split('*')
            return float(v1) * float(v2)
        elif self.variable_type == 'int' and '/' in self.variable_key:
            self.variable_key = self.variable_key.replace(match, str(self.real_variable_value))
            v1, v2 = self.variable_key.split('/')
            return float(v1) / float(v2)
        else:
            return self.real_variable_value

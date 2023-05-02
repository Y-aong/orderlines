# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : match.py
# Time       ：2023/2/22 21:58
# Author     ：blue_moon
# version    ：python 3.7
# Description：变量名匹配
"""
from order_lines.utils.exceptions import VariableException


class Match:
    def __init__(self, _variable_name: str):
        """
        这里变量有两种，变量指的是在流程里配置的${value},${add_value}+1
        同一个流程中的变量名是唯一的不可重复
        变量名目前只可以支持字母和下划线不支持数字
        变量指的是value和add_value
        :param _variable_name:
        """
        self._variable_name = _variable_name

    def variable_name(self) -> str:
        """
        获取变量名
        :return:变量名称
        """
        if any([True for item in self._variable_name if item in ['+', '-', '*', '/']]):
            # 这种是变量中存在+，-，*，/等四则运算
            variable_name = self.get_variable_name()
        else:
            variable_name = self._variable_name.replace('${', '').replace('}', '')
        return self.check_variable_name(variable_name)

    def get_variable_name(self):
        """从带有四则运行的变量中获取到变量名称"""
        if '${' not in self._variable_name and '}' not in self._variable_name:
            return self._variable_name
        if '+' in self._variable_name:
            match = [v for v in self._variable_name.split('+') if v.startswith('${') and v.endswith('}')].pop()
        elif '-' in self._variable_name:
            match = [v for v in self._variable_name.split('-') if v.startswith('${') and v.endswith('}')].pop()
        elif '*' in self._variable_name:
            match = [v for v in self._variable_name.split('*') if v.startswith('${') and v.endswith('}')].pop()
        elif '/' in self._variable_name:
            match = [v for v in self._variable_name.split('/') if v.startswith('${') and v.endswith('}')].pop()
        else:
            match = self._variable_name
        return match.replace('${', '').replace('}', '')

    def check_variable_name(self, variable_name):
        for temp in variable_name:
            if not temp.isalpha() and temp != '_':
                raise VariableException(f'{self.variable_name}设置错误，变量只能为字母和_组成')
        return variable_name

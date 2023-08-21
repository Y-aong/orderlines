# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Variable.py
# Time       ：2023/8/21 17:30
# Author     ：YangYong
# version    ：python 3.10
# Description：
    变量赋值
    Reassign a variable
"""
from typing import Any

from apis.orderlines.models import VariableInstance
from apis.orderlines.schema.variable_schema import VariableInstanceSchema
from conf.config import OrderLinesConfig
from orderlines.libraries.BaseTask import BaseTask
from orderlines.utils.base_orderlines_type import VariableParam
from public.base_model import get_session


class Variable(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self, process_instance_id: str):
        super(Variable, self).__init__()
        self.session = get_session()
        self.process_instance_id = process_instance_id

    @staticmethod
    def _handle_variable(variable_value: Any):
        """处理变量"""
        return variable_value

    def _update_cache_variable(self):
        """更新缓存的变量值,update cached variable values"""
        pass

    def variable_reassign(self, variable_param: VariableParam):
        """
        变量赋值，对于一个变量重新赋值新的值
        Variable assignment, reassigning a new value to a variable
        @param variable_param:
        @return:
        """
        variable_obj = self.session.query(VariableInstance).filter(
            VariableInstance.process_instance_id == self.process_instance_id,
            VariableInstance.variable_key == variable_param.variable_key
        ).first()
        if not variable_obj:
            variable_info = {
                'process_instance_id': self.process_instance_id,
                'variable_key': variable_param.variable_key,
                'variable_value': variable_param.variable_value,
                'variable_type': variable_param.variable_type
            }
            obj = VariableInstance(**variable_info)
            self.session.add(obj)
            self.session.commit()
        else:
            variable_info = VariableInstanceSchema().dump(variable_obj)
            if variable_info.get('is_cache'):
                # todo handle variable cache
                pass
            else:
                variable_value = variable_param.variable_value
                variable_value = self._handle_variable(variable_value)
                self.session.query(VariableInstance).filter(
                    VariableInstance.process_instance_id == self.process_instance_id,
                    VariableInstance.variable_key == variable_param.variable_key
                ).update(
                    {
                        'variable_key': variable_param.variable_key,
                        'variable_value': variable_value,
                        'variable_type': variable_param.variable_type,
                    }
                )
                self.session.commit()
        return {'status': self.success}

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : process_instance_view.py
# Time       ：2023/3/12 13:20
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    流程实例视图
    process instance view
"""
import datetime

from sqlalchemy import or_

from apis.orderlines.models import TaskInstance
from apis.orderlines.models.process import ProcessInstance
from apis.orderlines.schema.process_schema import ProcessInstanceSchema, ProcessInstanceExportSchema
from public.base_export_excel_view import BaseExportExcelView
from public.base_model import db
from public.base_view import BaseView


class ProcessInstanceView(BaseView):
    url = '/process_instance'

    def __init__(self):
        super(ProcessInstanceView, self).__init__()
        self.table_orm = ProcessInstance
        self.table_schema = ProcessInstanceSchema

    def handle_filter(self):
        self.filter.append(self.table_orm.active == 1)
        for key, val in self.form_data.items():
            if hasattr(self.table_orm, key) and val:
                self.filter.append(getattr(self.table_orm, key) == val)
            if key == 'keyword' and val:
                self.filter.append(or_(
                    self.table_orm.id == val,
                    self.table_orm.process_id == val,
                    self.table_orm.process_instance_id == val
                ))


class ProcessInstanceReportView(ProcessInstanceView, BaseExportExcelView):
    """普通流程导出, common process export"""
    url = '/process_instance/export'

    def __init__(self):
        super(ProcessInstanceReportView, self).__init__()
        self.file_name = f'process_instance_{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        self.columns = {
            'process_id': '流程id',
            'process_name': '流程名称',
            'process_params': '流程参数',
            'process_config': '流程配置',
            'start_time': '开始时间',
            'end_time': '结束时间',
            'runner': '运行者',
            'runner_id': '运行者id',
            'process_error_info': '流程异常信息',
            'process_status': '流程状态',
        }


class ProcessInstanceExcelReportView(BaseExportExcelView):
    """流程任务导出, process task export"""
    url = '/process_instance/excel/export'

    def __init__(self):
        super(ProcessInstanceExcelReportView, self).__init__()
        self.table_orm = ProcessInstance
        self.table_schema = ProcessInstanceExportSchema
        self.file_name = f'process_instance_{datetime.datetime.now().strftime("%Y-%m-%d")}'
        self.columns = {
            'process_id': '流程id',
            'process_name': '流程名称',
            'process_params': '流程参数',
            'process_config': '流程配置',
            'start_time': '开始时间',
            'end_time': '结束时间',
            'runner': '运行者',
            'runner_id': '运行者id',
            'process_error_info': '流程异常信息',
            'process_status': '流程状态',
            'task_name': '任务名称',
            'task_id': '任务id',
            'method_name': '函数名称',
            'task_kwargs': '任务参数',
            'task_result': '任务结果',
            'task_status': '任务状态',
        }

    def get_response(self):
        obj = db.session.query(
            ProcessInstance.process_id,
            ProcessInstance.process_name,
            ProcessInstance.process_params,
            ProcessInstance.process_config,
            ProcessInstance.start_time,
            ProcessInstance.end_time,
            ProcessInstance.runner,
            ProcessInstance.runner_id,
            ProcessInstance.process_error_info,
            ProcessInstance.process_status,
            TaskInstance.task_name,
            TaskInstance.task_id,
            TaskInstance.method_name,
            TaskInstance.method_kwargs,
            TaskInstance.task_result,
        ).join(TaskInstance, TaskInstance.process_instance_id == ProcessInstance.process_instance_id).filter(
            ProcessInstance.id == self.table_id
        ).all()
        self.response_data = ProcessInstanceExportSchema().dump(obj, many=True)

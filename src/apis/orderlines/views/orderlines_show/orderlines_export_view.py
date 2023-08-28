# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orderlines_export_view.py
# Time       ：2023/8/28 15:19
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
import os
from datetime import datetime

import pandas as pd
from flask import current_app, make_response, send_file
from jinja2 import FileSystemLoader, Environment

from apis.orderlines.models import ProcessInstance, TaskInstance
from apis.orderlines.schema.process_schema import ProcessInstanceSchema
from apis.orderlines.schema.task_schema import TaskInstanceSchema
from public.base_model import db
from public.base_view import BaseView


class ProcessInstanceHtmlReportView(BaseView):
    url = '/process_instance/html/export'

    def __init__(self):
        super(ProcessInstanceHtmlReportView, self).__init__()
        self.file_name = f'process_instance_{datetime.now().strftime("%Y-%m-%d")}.html'
        self.html_file_path = os.path.join(current_app.template_folder, self.file_name)

    def get_response(self):
        process_instance_obj = db.session.query(ProcessInstance).filter(ProcessInstance.id == self.table_id).first()
        process_instance_info = ProcessInstanceSchema().dump(process_instance_obj)

        task_instance_obj = db.session.query(TaskInstance).filter(
            TaskInstance.process_instance_id == process_instance_info.get('process_instance_id')).all()
        task_instance_info = TaskInstanceSchema().dump(task_instance_obj, many=True)
        df = pd.DataFrame(task_instance_info)
        response_data = dict()
        task_instance_info: list = df.to_dict('records')
        response_data.update(process_instance_info)
        response_data.setdefault('items', task_instance_info)
        return response_data

    def generate_html(self, data):
        env = Environment(loader=FileSystemLoader(current_app.template_folder))
        template = env.get_template('template.html')
        with open(self.html_file_path, 'w+', encoding='utf-8') as f:
            out = template.render(**data)
            f.write(out)
            f.close()

    def get(self):
        data = self.get_response()
        self.generate_html(data)
        response = make_response(send_file(self.html_file_path))
        response.headers["Content-Disposition"] = f"attachment; filename={self.file_name};"
        return response

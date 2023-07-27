# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : base_export_excel_view.py
# Time       ：2023/7/7 21:34
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    导出excel基类
    export excel base view
"""
import datetime
import io
from urllib.parse import quote

import pandas as pd
from flask import make_response, request

from public.api_handle_exception import handle_api_error
from public.base_view import BaseView


class BaseExportExcelView(BaseView):

    def __init__(self):
        super(BaseExportExcelView, self).__init__()
        self.form_data = request.args
        self.file_name = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.export_df = None
        self.response_data = None
        self.table_orm = None
        self.table_schema = None

    def get_response(self):
        self.handle_filter()
        self.response_data = self._get_multi()

    def make_response_date(self):
        self.get_response()
        self.export_df = pd.DataFrame(self.response_data)
        new_columns = list()
        old_columns = list()
        for column in self.export_df.columns:
            if self.columns.get(column):
                new_columns.append(self.columns.get(column))
                old_columns.append(column)
        self.export_df = self.export_df[old_columns]
        self.export_df.columns = new_columns

    @handle_api_error
    def get(self):
        self.make_response_date()
        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        self.export_df.to_excel(excel_writer=writer, index=False)
        writer.close()
        file_name = quote(self.file_name + '.xlsx')
        response = make_response(out.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename*=utf-8''{}".format(file_name)
        response.headers["Content-type"] = "application/x-xlsx"

        return response

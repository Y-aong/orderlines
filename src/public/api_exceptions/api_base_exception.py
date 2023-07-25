# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : api_base_exception.py
# Time       ：2023/1/11 20:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    接口异常基类
    api base exception
"""
import typing as t
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we make a mistakeO(∩_∩)O哈哈~'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, herders=None):

        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope: t.Optional[dict] = None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(
            self,
            environ=None,
            scope: t.Optional[dict] = None,
    ) -> t.List[t.Tuple[str, str]]:
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]

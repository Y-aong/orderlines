# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : api_exceptions.py
# Time       ：2023/1/11 20:54
# Author     ：Y-aong
# version    ：python 3.7
# Description：operators 异常类
"""
from .api_base_exception import APIException


class ClientException(APIException):
    code = 400
    msg = "client args error"
    error_code = 1001


class ParameterException(APIException):
    code = 400
    msg = "parameters error"
    error_code = 1002


class NotFundException(APIException):
    code = 404
    msg = "system_oauth not fund"
    error_code = 1003


class AuthException(APIException):
    code = 401
    msg = "authed failed"
    error_code = 1004


class JWTVerifyException(APIException):
    code = 401
    msg = "JWT Verify error"
    error_code = 1005


class Forbidden(APIException):
    code = 403
    msg = "Forbidden"
    error_code = 1006

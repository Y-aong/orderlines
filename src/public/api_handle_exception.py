# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : api_handle_exception.py
# Time       ：2023/7/7 21:29
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    处理api接口的装饰器
    Decorators that handle api interfaces
"""

import traceback

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from public.base_response import generate_abort
from public.logger import logger
from flask import request


def handle_api_error(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except IntegrityError as e:
            logger.info(f"request_url::{request.url},\ntraceback::{traceback.format_exc()}, {e}")
            return generate_abort(data=f'db parameter repetition::{e}', code=400)
        except ValueError as e:
            logger.info(f"request_url::{request.url},\ntraceback::{traceback.format_exc()}, {e}")
            return generate_abort(data=f'Client parameters are abnormal.{e}', code=400)
        except ValidationError as e:
            logger.info(f"request_url::{request.url},\ntraceback::{traceback.format_exc()}, {e}")
            return generate_abort(data=f'Client parameters are abnormal.{e}', code=400)
        except Exception as e:
            logger.info(f"request_url::{request.url},\ntraceback::{traceback.format_exc()}, {e}")
            return generate_abort(data='Server exception.', code=500)
        return res

    return wrapper

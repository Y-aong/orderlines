# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : jwt_utils.py
# Time       ：2023/7/9 16:45
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    jwt工具类
    jwt utils
"""
import datetime
import hashlib

import jwt
from flask import current_app
from jwt import ExpiredSignatureError, DecodeError

from conf.config import FlaskConfig
from public.api_exceptions.api_exceptions import JWTVerifyException


def encrypt_password(value: str) -> str:
    hash_lib = hashlib.md5()
    hash_lib.update(value.encode(encoding='utf8'))
    return hash_lib.hexdigest()


def generate_token(payload: dict, expiry: int, secret=None) -> str:
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=expiry)
    if not secret:
        secret = current_app.config["SECRET_KEY"]
    return jwt.encode(payload, secret, algorithm="HS256")


def verify_token(token, secret=None):
    if not secret:
        secret = current_app.config["SECRET_KEY"]
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
    except ExpiredSignatureError:
        raise JWTVerifyException("The current token has expired.")
    except DecodeError:
        raise DecodeError("jwt parse failed.")

    return payload


def refresh_token(token: str, secret=None):
    payload = verify_token(token, secret)
    return generate_token(payload, expiry=FlaskConfig.EXPIRY)

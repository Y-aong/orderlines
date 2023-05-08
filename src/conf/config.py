# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : config.py
# Time       ：2023/2/19 21:39
# Author     ：blue_moon
# version    ：python 3.7
# Description：配置文件类
"""
import os.path

import yaml


def read_yaml():
    current_path = os.path.dirname(os.path.realpath(__file__))
    yaml_dir_path = os.path.dirname(current_path)
    env = os.environ.get('ORDER_LINES')
    yaml_file = 'product_config.yaml' if env == 'product' else 'develop_config.yaml'
    yaml_path = os.path.join(yaml_dir_path, yaml_file)
    with open(yaml_path, mode='r', encoding='utf-8') as f:
        config_ctx = f.read()
    return config_ctx


class OrderLinesConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('order_lines')
    std_lib_location = _ctx.get('standard_library_location')
    callback_func = _ctx.get('callback_func')
    callback_module = _ctx.get('callback_module')
    retry_time = _ctx.get('retry_time')
    sleep_time = _ctx.get('sleep_time')
    task_timeout = _ctx.get('task_timeout')
    process_timeout = _ctx.get('process_timeout')


class EmailConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('email')
    is_send = _ctx.get('is_send')
    mail_host = _ctx.get('mail_host')
    mail_user = _ctx.get('mail_user')
    mail_pwd = _ctx.get('mail_pwd')
    sender = _ctx.get('sender')
    receivers = _ctx.get('receivers')


class CeleryConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('celery')
    enable_utc = _ctx.get('enable_utc')
    timezone = _ctx.get('timezone')
    beat_db_uri = _ctx.get('beat_db_uri')
    broker_url = _ctx.get('broker_url')
    result_backend = _ctx.get('result_backend')


class FlaskConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('flask')
    SQLALCHEMY_TRACK_MODIFICATIONS = _ctx.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_COMMIT_TEARDOWN = _ctx.get('SQLALCHEMY_COMMIT_TEARDOWN')
    SQLALCHEMY_DATABASE_URI = _ctx.get('SQLALCHEMY_DATABASE_URI')
    SECRET_KEY = _ctx.get('SECRET_KEY')
    PRE_PAGE = _ctx.get('PRE_PAGE')
    PAGE = _ctx.get('PAGE')


class LoggerConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('logger')
    linux_logger_path = _ctx.get('linux_logger_path')
    FMT = _ctx.get('FMT')
    DATE_FMT = _ctx.get('DATE_FMT')

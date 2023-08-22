# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : config.py
# Time       ：2023/2/19 21:39
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    配置文件类
    config model
"""
import os.path

import yaml


def read_yaml():
    current_path = os.path.dirname(os.path.realpath(__file__))
    yaml_dir_path = os.path.dirname(current_path)
    yaml_path = os.path.join(yaml_dir_path, 'config.yaml')
    with open(yaml_path, mode='r', encoding='utf-8') as f:
        config_ctx = f.read()
    return config_ctx


class Mysql:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('mysql')
    host = os.getenv('MYSQL_HOST') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('host')
    port = os.getenv('MYSQL_PORT') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('port')
    username = os.getenv('MYSQL_ROOT_USER') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('username')
    password = os.getenv('MYSQL_ROOT_PASSWORD') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('password')
    db = os.getenv('MYSQL_DATABASE') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('db')
    mysql_db_uri = f"mysql+pymysql://{username}:{password}@{host}:{port}/{db}"


class Mongo:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('mongodb')
    host = os.getenv('MONGODB_HOST') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('host')
    port = os.getenv('MONGODB_PORT') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('port')
    username = os.getenv('MONGODB_USERNAME') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('username')
    password = os.getenv('MONGODB_PASSWORD') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('password')
    db = os.getenv('MONGODB_DB') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('db')
    collection = os.getenv('MONGODB_COLLECTION') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('collection')


class Redis:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('redis')
    host = os.getenv('REDIS_HOST') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('host')
    port = os.getenv('REDIS_PORT') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('port')
    db = os.getenv('REDIS_DB') if os.getenv('ORDERLINES_ENV') == 'docker' else _ctx.get('db')
    broker_url = f"redis://{host}:{port}/{db}"
    result_backend = f"redis://{host}:{port}/{db}"


class OrderLinesConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('orderlines')
    std_lib_location = _ctx.get('standard_library_location')
    callback_func = _ctx.get('callback_func')
    callback_module = _ctx.get('callback_module')
    retry_time = _ctx.get('retry_time')
    sleep_time = _ctx.get('sleep_time')
    task_timeout = _ctx.get('task_timeout')
    process_timeout = _ctx.get('process_timeout')
    version = _ctx.get('version')
    task_strategy = _ctx.get('task_strategy')
    notice_type = _ctx.get('notice_type')


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
    beat_db_uri = Mysql.mysql_db_uri
    broker_url = Redis.broker_url
    result_backend = Redis.result_backend


class FlaskConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('flask')
    SQLALCHEMY_TRACK_MODIFICATIONS = _ctx.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_COMMIT_TEARDOWN = _ctx.get('SQLALCHEMY_COMMIT_TEARDOWN')
    SQLALCHEMY_DATABASE_URI = Mysql.mysql_db_uri
    EXPIRY = _ctx.get('EXPIRY')
    SECRET_KEY = _ctx.get('SECRET_KEY')


class LoggerConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('logger')
    logger_path = _ctx.get('logger_path')
    FMT = _ctx.get('FMT')
    DATE_FMT = _ctx.get('DATE_FMT')


class LanguageConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('language')
    language_type = _ctx.get('language_type')

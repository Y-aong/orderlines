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
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('orderlines')
    host = _ctx.get('host') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MYSQL_HOST')
    port = _ctx.get('port') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MYSQL_PORT')
    username = _ctx.get('username') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MYSQL_ROOT_USER')
    password = _ctx.get('password') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MYSQL_ROOT_PASSWORD')
    db = _ctx.get('db') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MYSQL_DATABASE')


class MongoConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('mongodb')
    host = _ctx.get('host') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_HOST')
    port = _ctx.get('port') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_PORT')
    username = _ctx.get('username') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_USERNAME')
    password = _ctx.get('password') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_PASSWORD')
    db = _ctx.get('db') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_DB')
    collection = _ctx.get('collection') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('MONGODB_COLLECTION')


class Redis:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('redis')
    host = _ctx.get('host') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('REDIS_HOST')
    port = _ctx.get('port') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('REDIS_PORT')
    db = _ctx.get('db') if os.getenv('ORDERLINES_ENV') != 'docker' else os.getenv('REDIS_DB')


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
    beat_db_uri = f"mysql+pymysql://{Mysql.username}:{Mysql.password}@{Mysql.host}:{Mysql.port}/{Mysql.db}"
    broker_url = f"redis://{Redis.host}:{Redis.port}/{Redis.db}"
    result_backend = f"redis://{Redis.host}:{Redis.port}/{Redis.db}"


class FlaskConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('flask')
    SQLALCHEMY_TRACK_MODIFICATIONS = _ctx.get('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_COMMIT_TEARDOWN = _ctx.get('SQLALCHEMY_COMMIT_TEARDOWN')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Mysql.username}:{Mysql.password}@{Mysql.host}:{Mysql.port}/{Mysql.db}"
    EXPIRY = 2 * 60 * 60
    SECRET_KEY = _ctx.get('SECRET_KEY')


class LoggerConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('logger')
    logger_path = _ctx.get('logger_path')
    FMT = _ctx.get('FMT')
    DATE_FMT = _ctx.get('DATE_FMT')


class LanguageConfig:
    _ctx: dict = yaml.load(read_yaml(), Loader=yaml.SafeLoader).get('language')
    language_type = _ctx.get('language_type')

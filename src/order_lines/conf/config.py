# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : config.py
# Time       ：2023/2/19 21:39
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import os.path

import yaml


def read_yaml():
    current_path = os.path.dirname(os.path.realpath(__file__))
    yaml_dir_path = os.path.dirname(os.path.dirname(current_path))
    yaml_path = os.path.join(yaml_dir_path, 'config.yaml')
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
    mail_host = _ctx.get('mail_host')
    mail_user = _ctx.get('mail_user')
    mail_pwd = _ctx.get('mail_pwd')
    sender = _ctx.get('sender')
    receivers = _ctx.get('receivers')

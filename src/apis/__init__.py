# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py
# Time       ：2023/2/19 21:05
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
import os.path

from celery import Celery
from flask import Flask

from public.api_utils.orderlines_plugin import OrderlinesPlugHelper
from public.api_utils.default_config_plugin import DefaultConfig
from public.api_utils.web_hook import WebHook

celery = Celery(__name__)
celery.config_from_object('tasks.celery_config')


def _register_plugin(app):
    default_config = DefaultConfig()
    default_config.init_app(app)
    OrderlinesPlugHelper().init_plugin()


def _register_webhook(app):
    web_hook = WebHook()
    web_hook.init_app(app)


def _register_db(app: Flask):
    from public.base_model import db
    from apis.orderlines.models import (
        ProcessInstance, Process, Task, TaskInstance, Variable, VariableInstance, PluginInfo, ScheduleTask, BaseConfig)
    from apis.schedule_plan.models import IntervalPlan, DatePlan, CrontabPlan, ApschedulerJobs
    from apis.system_oauth.models import (
        SystemUser, SystemRole, SystemPermission, SystemGroup, SystemDepartment, SystemUserRoleRelation,
        SystemUserGroupRelation, SystemGroupPermissionRelation, SystemRolePermissionRelation)

    db.init_app(app)
    with app.app_context():
        db.create_all()


def _register_resource(app):
    from apis.orderlines import order_line_blue
    from apis.schedule_plan import schedule_plan_blue
    from apis.system_oauth import system_oauth_blue

    app.register_blueprint(system_oauth_blue)
    app.register_blueprint(order_line_blue)
    app.register_blueprint(schedule_plan_blue)


def create_app():
    src_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template = os.path.join(src_file_path, 'templates')
    app = Flask(__name__, template_folder=template)
    app.config.from_object('conf.config.FlaskConfig')
    _register_db(app)
    _register_resource(app)
    # _register_webhook(app)
    _register_plugin(app)

    return app

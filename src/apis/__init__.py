# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py
# Time       ：2023/2/19 21:05
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from celery import Celery
from flask import Flask

celery = Celery(__name__)
celery.config_from_object('tasks.celery_config')


def _register_db(app: Flask):
    from public.base_model import db
    from apis.order_lines.models import TaskModel, TaskInstanceModel, ProcessInstanceModel, ProcessModel, VariableModel
    from apis.schedule_plan.models import IntervalPlan, DatePlan, CrontabPlan, ApschedulerJobs

    db.init_app(app)
    with app.app_context():
        db.create_all()


def _register_resource(app):
    from apis.order_lines import order_line_blue
    from apis.schedule_plan import schedule_plan_blue

    app.register_blueprint(order_line_blue)
    app.register_blueprint(schedule_plan_blue)


def create_app():
    app = Flask(__name__)
    app.config.from_object('conf.config.FlaskConfig')
    _register_db(app)
    _register_resource(app)
    return app

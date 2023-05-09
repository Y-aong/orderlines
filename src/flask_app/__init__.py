# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py
# Time       ：2023/2/19 21:05
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
from celery import Celery
from flask import Flask
from flask_restful import Api

celery = Celery(__name__)
celery.config_from_object('tasks.celery_config')


def _register_plugin(app: Flask):
    from flask_app.public.base_model import db
    from .celery_order_lines.models import (
        ProcessModel, ProcessInstanceModel, TaskModel, TaskInstanceModel, VariableModel, Test)
    db.init_app(app)
    with app.app_context():
        db.create_all()


def _register_resource(app):
    from flask_app.celery_order_lines.views import (
        TaskView, TaskInstanceView, ProcessView, ProcessInstanceView, OrderLinesBuildView, OrderLinesStart, TestView
    )

    api = Api(app)
    api.add_resource(TaskView, TaskView.url, endpoint='task')
    api.add_resource(TaskInstanceView, TaskInstanceView.url, endpoint='task_instance')
    api.add_resource(ProcessView, ProcessView.url, endpoint='process')
    api.add_resource(ProcessInstanceView, ProcessInstanceView.url, endpoint='process_instance')
    api.add_resource(OrderLinesBuildView, OrderLinesBuildView.url, endpoint='order_lines_build')
    api.add_resource(OrderLinesStart, OrderLinesStart.url, endpoint='order_lines_start')
    api.add_resource(TestView, TestView.url, endpoint='test')


def create_app():
    app = Flask(__name__)
    app.config.from_object('conf.config.FlaskConfig')
    _register_plugin(app)
    _register_resource(app)
    return app

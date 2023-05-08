# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : flask_main.py
# Time       ：2023/1/14 22:34
# Author     ：blue_moon
# version    ：python 3.7
# Description：flask方法入口
"""

from flask_app import create_app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_app.order_lines_app.models.order_line_models import db

app = create_app()
migrate = Migrate(app=app, db=db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # manager.run()
    app.run()

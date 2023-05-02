# !/usr/bin/env python


SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/order_lines'
SECRET_KEY = "051900abcsdafgdargdsf".encode("utf-8")

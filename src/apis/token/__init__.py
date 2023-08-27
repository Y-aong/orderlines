# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : __init__.py.py
# Time       ：2023/8/26 22:55
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
from flask import Blueprint
from flask_restful import Api

from apis.token.views.refresh_token_view import RefreshTokenView
from apis.token.views.register_view import RegisterView
from apis.token.views.token_view import TokenView
from apis.token.views.user_info_view import UserTokenView

token_blue = Blueprint("token", __name__, url_prefix="")
token_api = Api(token_blue)

token_api.add_resource(TokenView, TokenView.url)
token_api.add_resource(RefreshTokenView, RefreshTokenView.url)
token_api.add_resource(RegisterView, RegisterView.url)
token_api.add_resource(UserTokenView, UserTokenView.url)

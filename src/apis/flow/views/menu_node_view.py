# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : menu_node_view.py
# Time       ：2023/9/5 21:49
# Author     ：YangYong
# version    ：python 3.10
# Description：
    插件节点信息视图
"""
from flask import request

from flask_restful import Resource

from apis.config.models import PluginInfo
from apis.config.schema.plugin_info_schema import PluginNodeInfoSchema
from public.base_model import db
from public.base_response import generate_response


class NodeMenuView(Resource):
    url = '/node_menu'

    def __init__(self):
        self.form_data = request.args

    @staticmethod
    def get_nodes_type(title, plugin_info):
        for item in plugin_info:
            if item.get('title') == title:
                return item.get('class_name')
        return ''

    @staticmethod
    def get_nodes(title, plugin_info):
        nodes = list()
        for item in plugin_info:
            if item.get('title') == title:
                nodes.append({
                    'text': item.get('text'),
                    'type': item.get('type'),
                    'background': item.get('background'),
                    'method_name': item.get('method_name'),
                    'version': item.get('version'),
                    'class_name': item.get('class_name'),
                })
        return nodes

    def get_menu_nodes(self):
        plugin_nodes = list()
        objs = db.session.query(PluginInfo).all()
        plugin_info = PluginNodeInfoSchema().dump(objs, many=True)[::-1]
        titles = set([item.get('title') for item in plugin_info])
        _titles = list()
        sort_title = list()
        for temp in titles:
            if temp == '基础节点':
                sort_title.insert(0, temp)
            elif temp == '流程网关':
                sort_title.insert(1, temp)
            else:
                _titles.append(temp)
        _titles = sort_title + _titles

        for title in _titles:
            nodes = dict()
            nodes['title'] = title
            nodes['nodesType'] = self.get_nodes_type(title, plugin_info)
            nodes['nodes'] = self.get_nodes(title, plugin_info)
            plugin_nodes.append(nodes)
        return plugin_nodes

    def get(self):
        menu_nodes = self.get_menu_nodes()
        return generate_response(menu_nodes)

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : utils.py
# Time       ：2023/1/29 22:24
# Author     ：blue_moon
# version    ：python 3.7
# Description：order_line工具类
"""
import json
from typing import MutableMapping

from order_lines.utils.order_lines_types import is_string, is_dict_like


def get_current_node(task_id, process_node):
    """
    根据当前任务id获取当前正在运行的任务
    :return:当前的任务信息
    """
    for node in process_node:
        if node.get('task_id') == task_id:
            return node
    raise AttributeError(f'根据task id {task_id} 找不到任务节点')


def get_variable_value(variable_value, variable_type):
    if not variable_value:
        return None
    if variable_type == 'int':
        return int(variable_value)
    elif variable_type == 'str':
        return str(variable_value)
    elif variable_type == 'float':
        return float(variable_value)
    elif variable_type == 'bool':
        return bool(variable_value)
    elif variable_type == 'json':
        return json.dumps(variable_value)
    elif variable_type in 'dict':
        return json.loads(variable_value)
    else:
        return None


def normalize(string, ignore=(), caseless=True, spaceless=True):
    """Normalizes given string according to given spec.

    By default string is turned to lower case and all whitespace is removed.
    Additional characters can be removed by giving them in ``ignore`` list.
    """
    empty = '' if is_string(string) else b''
    if isinstance(ignore, bytes):
        # Iterating bytes in Python3 yields integers.
        ignore = [bytes([i]) for i in ignore]
    if spaceless:
        string = empty.join(string.split())
    if caseless:
        string = string.lower()
        ignore = [i.lower() for i in ignore]
    # both if statements below enhance performance a little
    if ignore:
        for ign in ignore:
            if ign in string:
                string = string.replace(ign, empty)
    return string


class NormalizedDict(MutableMapping):
    """Custom dictionary implementation automatically normalizing keys."""

    def __init__(self, initial=None, ignore=(), caseless=True, spaceless=True):
        """Initialized with possible initial value and normalizing spec.

        Initial values can be either a dictionary or an iterable of name/value
        pairs. In the latter case items are added in the given order.

        Normalizing spec has exact same semantics as with the :func:`normalize`
        function.
        """
        self._data = {}
        self._keys = {}
        self._normalize = lambda s: normalize(s, ignore, caseless, spaceless)
        if initial:
            self._add_initial(initial)

    def _add_initial(self, initial):
        items = initial.items() if hasattr(initial, 'items') else initial
        for key, value in items:
            self[key] = value

    def __getitem__(self, key):
        return self._data[self._normalize(key)]

    def __setitem__(self, key, value):
        norm_key = self._normalize(key)
        self._data[norm_key] = value
        self._keys.setdefault(norm_key, key)

    def __delitem__(self, key):
        norm_key = self._normalize(key)
        del self._data[norm_key]
        del self._keys[norm_key]

    def __iter__(self):
        return (self._keys[norm_key] for norm_key in sorted(self._keys))

    def __len__(self):
        return len(self._data)

    def __str__(self):
        return '{%s}' % ', '.join('%r: %r' % (key, self[key]) for key in self)

    def __eq__(self, other):
        if not is_dict_like(other):
            return False
        if not isinstance(other, NormalizedDict):
            other = NormalizedDict(other)
        return self._data == other._data

    def copy(self):
        copy = NormalizedDict()
        copy._data = self._data.copy()
        copy._keys = self._keys.copy()
        copy._normalize = self._normalize
        return copy

    # Speed-ups. Following methods are faster than default implementations.

    def __contains__(self, key):
        return self._normalize(key) in self._data

    def clear(self):
        self._data.clear()
        self._keys.clear()

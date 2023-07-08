# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : redis_test.py
# Time       ：2023/1/10 22:46
# Author     ：Y-aong
# version    ：python 3.7
# Description：任务运行节点时装饰器
"""
from typing import MutableMapping

from order_lines.utils.order_lines_types import is_dict_like
from order_lines.utils.utils import normalize


class NormalizedDict(MutableMapping):
    """自定义字典实现自动规范化组件库"""

    def __init__(self, initial=None, ignore=(), caseless=True, spaceless=True):
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

    def __contains__(self, key):
        return self._normalize(key) in self._data

    def clear(self):
        self._data.clear()
        self._keys.clear()

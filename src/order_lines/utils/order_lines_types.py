# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : order_lines_types.py
# Time       ：2023/2/19 20:02
# Author     ：blue_moon
# version    ：python 3.7
# Description：工作流中返回值的类型，这里有待改进，这里是参考robot-framework
"""
from collections.abc import Iterable, Mapping
from collections import UserString
from io import IOBase
from os import PathLike

try:
    from types import UnionType
except ImportError:  # Python < 3.10
    UnionType = ()
from typing import Union

try:
    from typing import TypedDict
except ImportError:  # Python < 3.8
    typeddict_types = ()
else:
    typeddict_types = (type(TypedDict('Dummy', {})),)
try:
    from typing_extensions import TypedDict as ExtTypedDict
except ImportError:
    pass
else:
    typeddict_types += (type(ExtTypedDict('Dummy', {})),)


def is_integer(item):
    return isinstance(item, int)


def is_number(item):
    return isinstance(item, (int, float))


def is_bytes(item):
    return isinstance(item, (bytes, bytearray))


def is_string(item):
    return isinstance(item, str)


def is_pathlike(item):
    return isinstance(item, PathLike)


def is_list_like(item):
    if isinstance(item, (str, bytes, bytearray, UserString, IOBase)):
        return False
    return isinstance(item, Iterable)


def is_dict_like(item):
    return isinstance(item, Mapping)


def is_union(item, allow_tuple=False):
    return (isinstance(item, UnionType)
            or getattr(item, '__origin__', None) is Union
            or (allow_tuple and isinstance(item, tuple)))

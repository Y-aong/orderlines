# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : variable_cache.py
# Time       ：2023/8/15 19:33
# Author     ：YangYong
# version    ：python 3.10
# Description：
    变量缓存
    variable cache
"""
from abc import ABC, abstractmethod
from typing import Any


class BaseVariableCache(ABC):

    @abstractmethod
    def get_cache_variable(self, variable_key: str) -> Any:
        pass

    @abstractmethod
    def set_cache_variable(self, variable_value: Any) -> str:
        pass


class RedisVariableCache(BaseVariableCache):
    def get_cache_variable(self, variable_key: str) -> Any:
        pass

    def set_cache_variable(self, variable_value: Any) -> str:
        pass


class MongoVariableCache(BaseVariableCache):
    def get_cache_variable(self, variable_key: str) -> Any:
        pass

    def set_cache_variable(self, variable_value: Any) -> str:
        pass

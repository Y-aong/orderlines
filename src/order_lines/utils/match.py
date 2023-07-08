# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : match.py
# Time       ：2023/2/19 20:46
# Author     ：Y-aong
# version    ：python 3.7
# Description：
"""
import fnmatch
import re
from functools import partial

from order_lines.utils.utils import normalize


class Matcher:

    def __init__(self, pattern, ignore=(), caseless=True, spaceless=True, regexp=False):
        self.pattern = pattern
        self._normalize = partial(normalize, ignore=ignore, caseless=caseless,
                                  spaceless=spaceless)
        self._regexp = self._compile(self._normalize(pattern), regexp=regexp)

    def _compile(self, pattern, regexp=False):
        if not regexp:
            pattern = fnmatch.translate(pattern)
        return re.compile(pattern, re.DOTALL)

    def match(self, string):
        return self._regexp.match(self._normalize(string)) is not None

    def match_any(self, strings):
        return any(self.match(s) for s in strings)

    def __bool__(self):
        return bool(self._normalize(self.pattern))

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : run_keyword_register.py
# Time       ：2023/2/19 19:59
# Author     ：blue_moon
# version    ：python 3.7
# Description：
"""
import warnings

from order_lines.utils.utils import NormalizedDict


class _RunKeywordRegister:

    def __init__(self):
        self._libs = {}

    def register_run_keyword(self, libname, keyword, args_to_process,
                             deprecation_warning=True, dry_run=False):
        """Deprecated API for registering "run keyword variants".

        Registered keywords are handled specially by Robot so that:

        - Their arguments are not resolved normally (use ``args_to_process``
          to control that). This mainly means replacing variables and handling
          escapes.
        - They are not stopped by timeouts.
        - If there are conflicts with keyword names, these keywords have
          *lower* precedence than other keywords.

        This API is pretty bad and will be reimplemented in the future.
        It is thus not considered stable, but external libraries can use it
        if they really need it and are aware of forthcoming breaking changes.

        Something like this is needed at least internally also in the future.
        For external libraries we hopefully could provide a better API for
        running keywords so that they would not need this in the first place.

        For more details see the following issues and issues linked from it:
        https://github.com/robotframework/robotframework/issues/2190

        :param libname: Name of the library the keyword belongs to.
        :param keyword: Name of the keyword itself.
        :param args_to_process: How many arguments to process normally before
            passing them to the keyword. Other arguments are not touched at all.
        :param dry_run: When true, this keyword is executed in dry run. Keywords
            to actually run are got based on the ``name`` argument these
            keywords must have.
        :param deprecation_warning: Set to ``False```to avoid the warning.
        """
        if deprecation_warning:
            warnings.warn(
                "The API to register run keyword variants and to disable variable "
                "resolving in keyword arguments will change in the future. "
                "For more information see "
                "https://github.com/robotframework/robotframework/issues/2190. "
                "Use with `deprecation_warning=False` to avoid this warning.",
                UserWarning
            )

        if libname not in self._libs:
            self._libs[libname] = NormalizedDict(ignore=['_'])
        self._libs[libname][keyword] = (int(args_to_process), dry_run)

    def get_args_to_process(self, libname, kwname):
        if libname in self._libs and kwname in self._libs[libname]:
            return self._libs[libname][kwname][0]
        return -1

    def get_dry_run(self, libname, kwname):
        if libname in self._libs and kwname in self._libs[libname]:
            return self._libs[libname][kwname][1]
        return False

    def is_run_keyword(self, libname, kwname):
        return self.get_args_to_process(libname, kwname) >= 0


RUN_KW_REGISTER = _RunKeywordRegister()

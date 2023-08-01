# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : running_strategy.py
# Time       ：2023/8/1 10:26
# Author     ：YangYong
# version    ：python 3.10
# Description：
    任务运行策略
    task run strategy when task run error
"""

from orderlines.real_running.app_context import AppContext
from orderlines.real_running.base_runner import BaseRunner
from orderlines.real_running.process_parse import ProcessParse


class RunningStrategy(BaseRunner):
    def __init__(
            self,
            process_instance_id: str,
            context: AppContext,
            current_task_id: str,
            parse: ProcessParse,
            timeout: int
    ):
        super(RunningStrategy, self).__init__(process_instance_id, context)
        self.task_config = context.get_task_node_item(process_instance_id, current_task_id, 'task_config')
        self.current_task_id = current_task_id
        self.parse = parse
        self.timeout = timeout
        self.strategy_context = {
            'RAISE': self.retry_strategy,
            'SKIP': self.skip_strategy,
            'RETRY': self.retry_strategy
        }

    def skip_strategy(self):
        pass

    def raise_strategy(self):
        pass

    def retry_strategy(self):
        pass

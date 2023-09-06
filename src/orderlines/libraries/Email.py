# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Email.py
# Time       ：2023/2/26 10:34
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    发送邮件, 用于任务失败回调
    Used for task failure callback
"""
import datetime
import smtplib

from email.mime.text import MIMEText

from conf.config import EmailConfig, OrderLinesConfig
from orderlines.libraries.BaseTask import BaseTask
from orderlines.utils.base_orderlines_type import EmailParam, EmailResult
from public.logger import logger
from orderlines.utils.orderlines_enum import TaskStatus


class Email(BaseTask):
    version = OrderLinesConfig.version

    def __init__(self):
        super(Email, self).__init__()
        self.mail_host = EmailConfig.mail_host
        self.mail_user = EmailConfig.mail_user
        self.mail_pwd = EmailConfig.mail_pwd
        self.sender = EmailConfig.sender
        self.receivers = EmailConfig.receivers
        self.error_status = {
            str(TaskStatus.red.value): 'run failure',
            str(TaskStatus.yellow.value): 'run stop',
            str(TaskStatus.pink.value): 'failure skip',
            str(TaskStatus.orange.value): 'failure retry',
        }

    def _build_msg(
            self,
            process_name: str,
            node_info: dict,
            error_or_result=None,
            status=None
    ) -> tuple:
        """构建发送邮件消息。Build mail message"""
        task_name = node_info.get("task_name")
        if status != TaskStatus.green.value:
            content = f'error info:{error_or_result}'
            title = f'process{process_name},task{task_name}{self.error_status.get(status, status)}'
        else:
            content = f'success:process run success,run result{error_or_result}'
            title = f'process:{process_name},task:{task_name}{self.error_status.get(status, status)}'
        msg = f'process_name:{process_name} \n' \
              f'task_name:{node_info.get("task_name")} \n' \
              f'method_kwargs:{node_info.get("method_kwargs")} \n' \
              f'run_time:{datetime.datetime.now()} \n' \
              f'{content}'
        return title, msg

    def send_msg(self, email_info: EmailParam) -> EmailResult:
        """
        邮件发送
        发送消息测试库，可用作回调方法
        Send message test library, which can be used as callback method
        :param email_info: email info
        :return:
        """
        if not EmailConfig.is_send:
            logger.info('The callback function was called successfully, and no mail was send')
            return {'status': TaskStatus.green.value}
        title, msg = self._build_msg(**email_info.model_dump())
        message = MIMEText(msg, 'plain', 'utf-8')
        message['Subject'] = title
        message['From'] = self.sender
        message['To'] = ','.join(self.receivers)
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.mail_host, 25)
            smtp_obj.login(self.mail_user, self.mail_pwd)
            smtp_obj.sendmail(self.sender, self.receivers, message.as_string())
            smtp_obj.quit()
            logger.info('email send success')
            return {'status': TaskStatus.green.value}
        except smtplib.SMTPException as e:
            logger.error(f'email send failure, error info:{e}')
            return {'status': TaskStatus.red.value}

# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : Email.py
# Time       ：2023/2/26 10:34
# Author     ：Y-aong
# version    ：python 3.7
# Description：发送邮件
"""
import datetime
import smtplib

from email.mime.text import MIMEText

from conf.config import EmailConfig, OrderLinesConfig
from order_lines.libraries.BaseTask import BaseTask
from order_lines.utils.base_orderlines_type import EmailParam, EmailResult
from public.logger import logger
from order_lines.utils.process_action_enum import StatusEnum


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
            str(StatusEnum.red.value): '运行失败',
            str(StatusEnum.pink.value): '失败跳过',
            str(StatusEnum.orange.value): '失败重试',
            str(StatusEnum.yellow.value): '运行超时',
        }

    def _build_msg(self, process_name: str, node_info: dict, error_or_result=None, status=None):
        """构建发送邮件信息"""
        task_name = node_info.get("task_name")
        if status != StatusEnum.green.value:
            content = f'错误信息:{error_or_result}'
            title = f'流程{process_name},任务{task_name}{self.error_status.get(status, status)}'
        else:
            content = f'运行信息:任务运行成功,运行结果{error_or_result}'
            title = f'流程{process_name},任务{task_name}{self.error_status.get(status, status)}'
        msg = f'流程名称:{process_name} \n' \
              f'任务名称:{node_info.get("task_name")} \n' \
              f'任务参数:{node_info.get("method_kwargs")} \n' \
              f'运行时间:{datetime.datetime.now()} \n' \
              f'{content}'
        return title, msg

    def send_msg(self, email_info: EmailParam) -> EmailResult:
        """
        发送消息测试库，可以作为callback方法
        :param email_info: 邮件信息
        :return:
        """
        if not EmailConfig.is_send:
            logger.info('回调函数调用成功，不发送邮件')
            return {'status': StatusEnum.green.value}
        title, msg = self._build_msg(**email_info.model_dump())
        message = MIMEText(msg, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = self.sender
        # 接受方信息
        message['To'] = ','.join(self.receivers)
        # 登录并发送邮件
        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.mail_host, 25)
            smtp_obj.login(self.mail_user, self.mail_pwd)
            smtp_obj.sendmail(self.sender, self.receivers, message.as_string())
            smtp_obj.quit()
            logger.info('邮件发送成功')
            return {'status': StatusEnum.green.value}
        except smtplib.SMTPException as e:
            logger.error(f'邮件发送失败, 异常信息:{e}')
            return {'status': StatusEnum.red.value}

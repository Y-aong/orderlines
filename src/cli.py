# !/usr/bin/env python
# -*-coding:utf-8 -*-
"""
# File       : cli.py
# Time       ：2023/8/19 15:43
# Author     ：Y-aong
# version    ：python 3.7
# Description：
    orderlines命令行功能
"""
import os

import click

from apis import create_app
from grpc_api.orderlines_grpc_server import grpc_server
from orderlines import OrderLines
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter
from public.api_utils.default_config_plugin import DefaultConfig
from public.schedule_utils.apscheduler_config import scheduler


class Config:

    def __init__(self):
        self.path = os.getcwd()
        self.aliases = {}

    def add_alias(self, alias, cmd):
        self.aliases.update({alias: cmd})


pass_config = click.make_pass_decorator(Config, ensure=True)


class OrderlinesGroup(click.Group):

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        cfg = ctx.ensure_object(Config)

        if cmd_name in cfg.aliases:
            actual_cmd = cfg.aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)
        matches = [
            x for x in self.list_commands(ctx) if x.lower().startswith(cmd_name.lower())
        ]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail(f"Too many matches: {', '.join(sorted(matches))}")

    def resolve_command(self, ctx, args):
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


@click.command(cls=OrderlinesGroup)
def cli():
    """orderlines keep the process organized."""


@cli.command()
@click.option('-p_id', '--process_id', type=str, help='process id.')
@click.option('-id', '--process_table_id', type=str, help='process table id.')
@click.option('--dry', type=bool, default=False, help='True——not insert into db, False——insert into db.')
@click.option('--run_type', type=click.Choice(['schedule', 'trigger']), default='trigger', help='schedule or trigger.')
@click.option('--clear_db', type=bool, default=False,
              help='only test, if True will clear table,'
                   'process,process instance,task,task_instance variable,variable_instance.')
def start_process(process_id=None, process_table_id=None, dry=False, run_type='trigger', clear_db=False):
    """start process by process instance id."""
    if process_id:
        process_id = process_id
    elif process_table_id:
        process_id = process_table_id
    else:
        raise ValueError('process_id, process_table_id there must be one')
    OrderLines().start(process_id=process_id, dry=dry, run_type=run_type, clear_db=clear_db)


@cli.command()
@click.option('-ps_id', '--process_instance_id', required=True, type=str, help='want stop process instance id.')
@click.option('--stop_schedule', type=bool, default=False, help='if true stop schedule task,default false.')
def stop_process(process_instance_id, stop_schedule=False):
    """stop process by process instance id."""
    OrderLines().stop_process(process_instance_id=process_instance_id, stop_schedule=stop_schedule)


@cli.command()
@click.option('-ps_id', '--process_instance_id', required=True, type=str, help='want pause process instance id.')
@click.option('--stop_schedule', type=bool, default=False, help='if true stop schedule task,default false.')
def paused_process(process_instance_id, stop_schedule=False):
    """pause process by process instance id."""
    OrderLines().paused_process(process_instance_id=process_instance_id, stop_schedule=stop_schedule)


@cli.command()
@click.option('-ps_id', '--process_instance_id', required=True, type=str, help='want recover process instance id.')
@click.option('--recover_schedule', type=bool, default=False, help='if true recover schedule task,default false,')
def recover_process(process_instance_id, recover_schedule=False):
    """recover process by process instance id."""
    OrderLines().recover_process(process_instance_id=process_instance_id, recover_schedule=recover_schedule)


@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="The interface to bind to.")
@click.option("--port", "-p", default=15900, help="The port to bind to.")
def runserver(host, port):
    """run orderlines server, default port 15900."""
    app = create_app()
    app.run(host=host, port=port)


@cli.command()
def schedule():
    """start schedule plan."""
    scheduler.start()


@cli.command()
@click.option("--filename", "-f", type=click.Path(exists=True), help="the json file path to build process.")
def build_process_by_json(filename):
    """build process by json file."""
    ProcessBuildAdapter().build_by_json(filename)
    click.echo('process build success')


@cli.command()
@click.option("--filename", "-f", type=click.Path(exists=True), help="the yaml file path to build process.")
def build_process_by_yaml(filename):
    """build process by yaml file."""
    ProcessBuildAdapter().build_by_yaml(filename)
    click.echo('process build success')


@cli.command()
@click.option("--username", "-u", default="orderlines", help="super user username default orderlines.")
@click.option("--password", "-p", default="orderlines", help="super user password default orderlines.")
@click.option("--email", default="", help="super user email default None.")
@click.option("--phone", default="", help="super user phone default None.")
def create_super_user(username, password, email, phone):
    """create a super administrator."""
    DefaultConfig().create_user(username, password, email, phone, admin=True)


@cli.command()
@click.option("--username", "-u", help="common user username.")
@click.option("--password", "-p", help="common super user password.")
@click.option("--email", default="", help="super user email default None.")
@click.option("--phone", default="", help="super user phone default None.")
def create_user(username, password, email, phone):
    """create a super administrator."""
    DefaultConfig().create_user(username, password, email, phone, admin=False)


@cli.command()
@click.option("--host", "-h", default="0.0.0.0", help="The grpc server interface to bind to.")
@click.option("--port", "-p", default=50051, help="The grpc server port to bind to.")
def run_grpc(host, port):
    """run grpc server."""
    grpc_server(host, port)

# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : grpc_client.py
# Time       ：2023/8/21 16:16
# Author     ：YangYong
# version    ：python 3.10
# Description：
"""
import os.path

import grpc

from grpc_api.grpc_proto import orderlines_pb2
from grpc_api.grpc_proto import orderlines_pb2_grpc


def grpc_client_start():
    with grpc.insecure_channel('localhost:50051') as channel:
        stud = orderlines_pb2_grpc.OrderlinesServiceStub(channel)
        # start process
        response = stud.StartProcess(
            orderlines_pb2.StartRequest(
                process_id='10002',
                run_type='trigger',
                dry=False,
                clear_db=False
            )
        )
        print(f'start process response {response}')


def grpc_client_build_by_json():
    # build process by json
    with grpc.insecure_channel('localhost:50051') as channel:
        stud = orderlines_pb2_grpc.OrderlinesServiceStub(channel)
        response = stud.BuildProcessByJson(
            orderlines_pb2.BuildProcessByJsonRequest(
                filepath=os.path.abspath('./data/process.json'),
                clear_db=True
            )
        )
        print(f'build process by json response {response}')


grpc_client_start()

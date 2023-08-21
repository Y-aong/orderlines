# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : orderlines_grpc_server.py
# Time       ：2023/8/21 15:19
# Author     ：YangYong
# version    ：python 3.10
# Description：
    orderlines grpc server
    python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. .\orderlines.proto
"""
import traceback

import grpc

from concurrent import futures
import time

from grpc_api.grpc_proto import orderlines_pb2_grpc
from grpc_api.grpc_proto import orderlines_pb2
from orderlines import OrderLines
from orderlines.process_build.process_build_adapter import ProcessBuildAdapter
from public.logger import logger

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def generate_grpc_response(code: int = 200, msg: str = 'success!', **kwargs):
    response = {'code': code, 'message': msg}
    response.update(kwargs)
    return response


class OrderLinesServicer(orderlines_pb2_grpc.OrderlinesServiceServicer):

    def __init__(self):
        self.orderlines = OrderLines()

    def StartProcess(self, request, context):
        try:
            process_instance_id = self.orderlines.start(
                process_id=request.process_id,
                run_type=request.run_type,
                dry=request.dry,
                clear_db=request.clear_db
            )
            response = generate_grpc_response(msg='process start success', process_instance_id=process_instance_id)
            return orderlines_pb2.StartResponse(**response)
        except Exception as e:
            logger.error(f'grpc start process error. {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'start error, {e}.', process_instance_id='')
            return orderlines_pb2.StartResponse(**response)

    def StopProcess(self, request, context):
        try:
            self.orderlines.stop_process(request.process_instance_id, request.stop_schedule)
            response = generate_grpc_response(200, 'process stop success')
            return orderlines_pb2.ProcessOperatorResponse(**response)
        except Exception as e:
            logger.error(f'grpc stop process error. {traceback.format_exc()}')
            response = generate_grpc_response(500, f'grpc stop process error, {e}.')
            return orderlines_pb2.ProcessOperatorResponse(**response)

    def PausedProcess(self, request, context):
        try:
            self.orderlines.paused_process(request.process_instance_id, request.stop_schedule)
            response = generate_grpc_response(200, 'process paused success')
            return orderlines_pb2.ProcessOperatorResponse(**response)
        except Exception as e:
            logger.error(f'grpc paused process error, {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'process stop error, {e}.')
            return orderlines_pb2.ProcessOperatorResponse(**response)

    def RecoverProcess(self, request, context):
        try:
            self.orderlines.recover_process(request.process_instance_id, request.recover_schedule)
            response = generate_grpc_response(200, 'process recover success')
            return orderlines_pb2.ProcessOperatorResponse(**response)
        except Exception as e:
            logger.error(f'grpc paused process error. {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'process recover error, {e}.')
            return orderlines_pb2.ProcessOperatorResponse(**response)

    def BuildProcessByJson(self, request, context):
        try:
            process_id = ProcessBuildAdapter().build_by_json(request.filepath, request.clear_db)
            response = generate_grpc_response(200, 'process build success', process_id=process_id)
            return orderlines_pb2.BuildProcessResponse(**response)
        except Exception as e:
            logger.error(f'build process error. {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'process build error, {e}.', process_id='')
            return orderlines_pb2.BuildProcessResponse(**response)

    def BuildProcessByYaml(self, request, context):
        try:
            process_id = ProcessBuildAdapter().build_by_yaml(request.filepath, request.clear_db)
            response = generate_grpc_response(200, 'process build success', process_id=process_id)
            return orderlines_pb2.BuildProcessResponse(**response)
        except Exception as e:
            logger.error(f'build process error. {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'process build error, {e}.', process_id='')
            return orderlines_pb2.BuildProcessResponse(**response)

    def BuildProcessByDict(self, request, context):
        try:
            process_id = ProcessBuildAdapter().build_by_dict(
                process_info=request.process_info,
                task_nodes=request.task_nodes,
                variable=request.variable,
                clear_db=request.clear_db
            )
            response = generate_grpc_response(200, 'process build success', process_id=process_id)
            return orderlines_pb2.BuildProcessResponse(**response)
        except Exception as e:
            logger.error(f'build process error. {traceback.format_exc()}.')
            response = generate_grpc_response(500, f'process build error, {e}.', process_id='')
            return orderlines_pb2.BuildProcessResponse(**response)


def grpc_server(host: str, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    orderlines_pb2_grpc.add_OrderlinesServiceServicer_to_server(OrderLinesServicer(), server)
    server.add_insecure_port(f'{host}:{port}')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

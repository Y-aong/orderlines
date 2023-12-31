# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpc_api.grpc_proto.orderlines_pb2 as orderlines__pb2


class OrderlinesServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartProcess = channel.unary_unary(
                '/OrderlinesService/StartProcess',
                request_serializer=orderlines__pb2.StartRequest.SerializeToString,
                response_deserializer=orderlines__pb2.StartResponse.FromString,
                )
        self.StopProcess = channel.unary_unary(
                '/OrderlinesService/StopProcess',
                request_serializer=orderlines__pb2.ProcessOperatorRequest.SerializeToString,
                response_deserializer=orderlines__pb2.ProcessStopResponse.FromString,
                )
        self.PausedProcess = channel.unary_unary(
                '/OrderlinesService/PausedProcess',
                request_serializer=orderlines__pb2.ProcessOperatorRequest.SerializeToString,
                response_deserializer=orderlines__pb2.ProcessOperatorResponse.FromString,
                )
        self.RecoverProcess = channel.unary_unary(
                '/OrderlinesService/RecoverProcess',
                request_serializer=orderlines__pb2.ProcessRecoverRequest.SerializeToString,
                response_deserializer=orderlines__pb2.ProcessOperatorResponse.FromString,
                )
        self.BuildProcessByJson = channel.unary_unary(
                '/OrderlinesService/BuildProcessByJson',
                request_serializer=orderlines__pb2.BuildProcessByJsonRequest.SerializeToString,
                response_deserializer=orderlines__pb2.BuildProcessResponse.FromString,
                )
        self.BuildProcessByYaml = channel.unary_unary(
                '/OrderlinesService/BuildProcessByYaml',
                request_serializer=orderlines__pb2.BuildProcessByYamlRequest.SerializeToString,
                response_deserializer=orderlines__pb2.BuildProcessResponse.FromString,
                )
        self.BuildProcessByDict = channel.unary_unary(
                '/OrderlinesService/BuildProcessByDict',
                request_serializer=orderlines__pb2.BuildProcessByDictRequest.SerializeToString,
                response_deserializer=orderlines__pb2.BuildProcessResponse.FromString,
                )


class OrderlinesServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StartProcess(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopProcess(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PausedProcess(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RecoverProcess(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuildProcessByJson(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuildProcessByYaml(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuildProcessByDict(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_OrderlinesServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartProcess': grpc.unary_unary_rpc_method_handler(
                    servicer.StartProcess,
                    request_deserializer=orderlines__pb2.StartRequest.FromString,
                    response_serializer=orderlines__pb2.StartResponse.SerializeToString,
            ),
            'StopProcess': grpc.unary_unary_rpc_method_handler(
                    servicer.StopProcess,
                    request_deserializer=orderlines__pb2.ProcessOperatorRequest.FromString,
                    response_serializer=orderlines__pb2.ProcessStopResponse.SerializeToString,
            ),
            'PausedProcess': grpc.unary_unary_rpc_method_handler(
                    servicer.PausedProcess,
                    request_deserializer=orderlines__pb2.ProcessOperatorRequest.FromString,
                    response_serializer=orderlines__pb2.ProcessOperatorResponse.SerializeToString,
            ),
            'RecoverProcess': grpc.unary_unary_rpc_method_handler(
                    servicer.RecoverProcess,
                    request_deserializer=orderlines__pb2.ProcessRecoverRequest.FromString,
                    response_serializer=orderlines__pb2.ProcessOperatorResponse.SerializeToString,
            ),
            'BuildProcessByJson': grpc.unary_unary_rpc_method_handler(
                    servicer.BuildProcessByJson,
                    request_deserializer=orderlines__pb2.BuildProcessByJsonRequest.FromString,
                    response_serializer=orderlines__pb2.BuildProcessResponse.SerializeToString,
            ),
            'BuildProcessByYaml': grpc.unary_unary_rpc_method_handler(
                    servicer.BuildProcessByYaml,
                    request_deserializer=orderlines__pb2.BuildProcessByYamlRequest.FromString,
                    response_serializer=orderlines__pb2.BuildProcessResponse.SerializeToString,
            ),
            'BuildProcessByDict': grpc.unary_unary_rpc_method_handler(
                    servicer.BuildProcessByDict,
                    request_deserializer=orderlines__pb2.BuildProcessByDictRequest.FromString,
                    response_serializer=orderlines__pb2.BuildProcessResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'OrderlinesService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class OrderlinesService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StartProcess(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/StartProcess',
            orderlines__pb2.StartRequest.SerializeToString,
            orderlines__pb2.StartResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def StopProcess(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/StopProcess',
            orderlines__pb2.ProcessOperatorRequest.SerializeToString,
            orderlines__pb2.ProcessStopResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PausedProcess(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/PausedProcess',
            orderlines__pb2.ProcessOperatorRequest.SerializeToString,
            orderlines__pb2.ProcessOperatorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RecoverProcess(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/RecoverProcess',
            orderlines__pb2.ProcessRecoverRequest.SerializeToString,
            orderlines__pb2.ProcessOperatorResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuildProcessByJson(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/BuildProcessByJson',
            orderlines__pb2.BuildProcessByJsonRequest.SerializeToString,
            orderlines__pb2.BuildProcessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuildProcessByYaml(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/BuildProcessByYaml',
            orderlines__pb2.BuildProcessByYamlRequest.SerializeToString,
            orderlines__pb2.BuildProcessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuildProcessByDict(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/OrderlinesService/BuildProcessByDict',
            orderlines__pb2.BuildProcessByDictRequest.SerializeToString,
            orderlines__pb2.BuildProcessResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from pythie_serving.tensorflow_proto.tensorflow_serving.apis import get_model_status_pb2 as tensorflow__serving_dot_apis_dot_get__model__status__pb2
from pythie_serving.tensorflow_proto.tensorflow_serving.apis import model_management_pb2 as tensorflow__serving_dot_apis_dot_model__management__pb2


class ModelServiceStub(object):
  """ModelService provides methods to query and update the state of the server,
  e.g. which models/versions are being served.
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetModelStatus = channel.unary_unary(
        '/tensorflow.serving.ModelService/GetModelStatus',
        request_serializer=tensorflow__serving_dot_apis_dot_get__model__status__pb2.GetModelStatusRequest.SerializeToString,
        response_deserializer=tensorflow__serving_dot_apis_dot_get__model__status__pb2.GetModelStatusResponse.FromString,
        )
    self.HandleReloadConfigRequest = channel.unary_unary(
        '/tensorflow.serving.ModelService/HandleReloadConfigRequest',
        request_serializer=tensorflow__serving_dot_apis_dot_model__management__pb2.ReloadConfigRequest.SerializeToString,
        response_deserializer=tensorflow__serving_dot_apis_dot_model__management__pb2.ReloadConfigResponse.FromString,
        )


class ModelServiceServicer(object):
  """ModelService provides methods to query and update the state of the server,
  e.g. which models/versions are being served.
  """

  def GetModelStatus(self, request, context):
    """Gets status of model. If the ModelSpec in the request does not specify
    version, information about all versions of the model will be returned. If
    the ModelSpec in the request does specify a version, the status of only
    that version will be returned.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def HandleReloadConfigRequest(self, request, context):
    """Reloads the set of served models. The new config supersedes the old one,
    so if a model is omitted from the new config it will be unloaded and no
    longer served.
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ModelServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetModelStatus': grpc.unary_unary_rpc_method_handler(
          servicer.GetModelStatus,
          request_deserializer=tensorflow__serving_dot_apis_dot_get__model__status__pb2.GetModelStatusRequest.FromString,
          response_serializer=tensorflow__serving_dot_apis_dot_get__model__status__pb2.GetModelStatusResponse.SerializeToString,
      ),
      'HandleReloadConfigRequest': grpc.unary_unary_rpc_method_handler(
          servicer.HandleReloadConfigRequest,
          request_deserializer=tensorflow__serving_dot_apis_dot_model__management__pb2.ReloadConfigRequest.FromString,
          response_serializer=tensorflow__serving_dot_apis_dot_model__management__pb2.ReloadConfigResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'tensorflow.serving.ModelService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow_serving/core/logging.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow_serving.apis import model_pb2 as tensorflow__serving_dot_apis_dot_model__pb2
from pythie_serving.tensorflow_proto.tensorflow_serving.config import logging_config_pb2 as tensorflow__serving_dot_config_dot_logging__config__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow_serving/core/logging.proto',
  package='tensorflow.serving',
  syntax='proto3',
  serialized_options=_b('\370\001\001'),
  serialized_pb=_b('\n%tensorflow_serving/core/logging.proto\x12\x12tensorflow.serving\x1a#tensorflow_serving/apis/model.proto\x1a.tensorflow_serving/config/logging_config.proto\"\x97\x01\n\x0bLogMetadata\x12\x31\n\nmodel_spec\x18\x01 \x01(\x0b\x32\x1d.tensorflow.serving.ModelSpec\x12;\n\x0fsampling_config\x18\x02 \x01(\x0b\x32\".tensorflow.serving.SamplingConfig\x12\x18\n\x10saved_model_tags\x18\x03 \x03(\tB\x03\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorflow__serving_dot_apis_dot_model__pb2.DESCRIPTOR,tensorflow__serving_dot_config_dot_logging__config__pb2.DESCRIPTOR,])




_LOGMETADATA = _descriptor.Descriptor(
  name='LogMetadata',
  full_name='tensorflow.serving.LogMetadata',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='model_spec', full_name='tensorflow.serving.LogMetadata.model_spec', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sampling_config', full_name='tensorflow.serving.LogMetadata.sampling_config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='saved_model_tags', full_name='tensorflow.serving.LogMetadata.saved_model_tags', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=298,
)

_LOGMETADATA.fields_by_name['model_spec'].message_type = tensorflow__serving_dot_apis_dot_model__pb2._MODELSPEC
_LOGMETADATA.fields_by_name['sampling_config'].message_type = tensorflow__serving_dot_config_dot_logging__config__pb2._SAMPLINGCONFIG
DESCRIPTOR.message_types_by_name['LogMetadata'] = _LOGMETADATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

LogMetadata = _reflection.GeneratedProtocolMessageType('LogMetadata', (_message.Message,), {
  'DESCRIPTOR' : _LOGMETADATA,
  '__module__' : 'tensorflow_serving.core.logging_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.serving.LogMetadata)
  })
_sym_db.RegisterMessage(LogMetadata)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

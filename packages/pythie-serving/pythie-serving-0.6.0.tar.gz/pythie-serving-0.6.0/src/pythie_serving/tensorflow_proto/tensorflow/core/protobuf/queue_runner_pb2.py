# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/queue_runner.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow.core.lib.core import error_codes_pb2 as tensorflow_dot_core_dot_lib_dot_core_dot_error__codes__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/queue_runner.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=_b('\n\030org.tensorflow.frameworkB\021QueueRunnerProtosP\001Z<github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf\370\001\001'),
  serialized_pb=_b('\n+tensorflow/core/protobuf/queue_runner.proto\x12\ntensorflow\x1a*tensorflow/core/lib/core/error_codes.proto\"\xaa\x01\n\x0eQueueRunnerDef\x12\x12\n\nqueue_name\x18\x01 \x01(\t\x12\x17\n\x0f\x65nqueue_op_name\x18\x02 \x03(\t\x12\x15\n\rclose_op_name\x18\x03 \x01(\t\x12\x16\n\x0e\x63\x61ncel_op_name\x18\x04 \x01(\t\x12<\n\x1cqueue_closed_exception_types\x18\x05 \x03(\x0e\x32\x16.tensorflow.error.CodeBp\n\x18org.tensorflow.frameworkB\x11QueueRunnerProtosP\x01Z<github.com/tensorflow/tensorflow/tensorflow/go/core/protobuf\xf8\x01\x01\x62\x06proto3')
  ,
  dependencies=[tensorflow_dot_core_dot_lib_dot_core_dot_error__codes__pb2.DESCRIPTOR,])




_QUEUERUNNERDEF = _descriptor.Descriptor(
  name='QueueRunnerDef',
  full_name='tensorflow.QueueRunnerDef',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='queue_name', full_name='tensorflow.QueueRunnerDef.queue_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='enqueue_op_name', full_name='tensorflow.QueueRunnerDef.enqueue_op_name', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='close_op_name', full_name='tensorflow.QueueRunnerDef.close_op_name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cancel_op_name', full_name='tensorflow.QueueRunnerDef.cancel_op_name', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='queue_closed_exception_types', full_name='tensorflow.QueueRunnerDef.queue_closed_exception_types', index=4,
      number=5, type=14, cpp_type=8, label=3,
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
  serialized_start=104,
  serialized_end=274,
)

_QUEUERUNNERDEF.fields_by_name['queue_closed_exception_types'].enum_type = tensorflow_dot_core_dot_lib_dot_core_dot_error__codes__pb2._CODE
DESCRIPTOR.message_types_by_name['QueueRunnerDef'] = _QUEUERUNNERDEF
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

QueueRunnerDef = _reflection.GeneratedProtocolMessageType('QueueRunnerDef', (_message.Message,), {
  'DESCRIPTOR' : _QUEUERUNNERDEF,
  '__module__' : 'tensorflow.core.protobuf.queue_runner_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.QueueRunnerDef)
  })
_sym_db.RegisterMessage(QueueRunnerDef)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

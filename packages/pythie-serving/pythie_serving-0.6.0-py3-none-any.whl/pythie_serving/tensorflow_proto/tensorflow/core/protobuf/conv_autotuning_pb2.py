# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/conv_autotuning.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow.stream_executor import dnn_pb2 as tensorflow_dot_stream__executor_dot_dnn__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/protobuf/conv_autotuning.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n.tensorflow/core/protobuf/conv_autotuning.proto\x12\ntensorflow\x1a$tensorflow/stream_executor/dnn.proto\"\x9d\x04\n\x10\x43onvolutionProto\x12\x32\n\x04kind\x18\x01 \x01(\x0e\x32$.stream_executor.dnn.ConvolutionKind\x12\x39\n\x05input\x18\x02 \x01(\x0b\x32*.stream_executor.dnn.TensorDescriptorProto\x12:\n\x06\x66ilter\x18\x03 \x01(\x0b\x32*.stream_executor.dnn.TensorDescriptorProto\x12:\n\x06output\x18\x04 \x01(\x0b\x32*.stream_executor.dnn.TensorDescriptorProto\x12\x42\n\tconv_desc\x18\x05 \x01(\x0b\x32/.stream_executor.dnn.ConvolutionDescriptorProto\x12\x12\n\nconv_scale\x18\x06 \x01(\x01\x12\x18\n\x10side_value_scale\x18\x07 \x01(\x01\x12\x37\n\nactivation\x18\x08 \x01(\x0e\x32#.stream_executor.dnn.ActivationMode\x12\x15\n\rinput_address\x18\t \x01(\x03\x12\x16\n\x0e\x66ilter_address\x18\n \x01(\x03\x12\x16\n\x0eoutput_address\x18\x0b \x01(\x03\x12\x14\n\x0c\x62ias_address\x18\x0c \x01(\x03\x12\x1a\n\x12side_input_address\x18\r \x01(\x03\x62\x06proto3')
  ,
  dependencies=[tensorflow_dot_stream__executor_dot_dnn__pb2.DESCRIPTOR,])




_CONVOLUTIONPROTO = _descriptor.Descriptor(
  name='ConvolutionProto',
  full_name='tensorflow.ConvolutionProto',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='kind', full_name='tensorflow.ConvolutionProto.kind', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input', full_name='tensorflow.ConvolutionProto.input', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter', full_name='tensorflow.ConvolutionProto.filter', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output', full_name='tensorflow.ConvolutionProto.output', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conv_desc', full_name='tensorflow.ConvolutionProto.conv_desc', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='conv_scale', full_name='tensorflow.ConvolutionProto.conv_scale', index=5,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='side_value_scale', full_name='tensorflow.ConvolutionProto.side_value_scale', index=6,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='activation', full_name='tensorflow.ConvolutionProto.activation', index=7,
      number=8, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='input_address', full_name='tensorflow.ConvolutionProto.input_address', index=8,
      number=9, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter_address', full_name='tensorflow.ConvolutionProto.filter_address', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_address', full_name='tensorflow.ConvolutionProto.output_address', index=10,
      number=11, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='bias_address', full_name='tensorflow.ConvolutionProto.bias_address', index=11,
      number=12, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='side_input_address', full_name='tensorflow.ConvolutionProto.side_input_address', index=12,
      number=13, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=101,
  serialized_end=642,
)

_CONVOLUTIONPROTO.fields_by_name['kind'].enum_type = tensorflow_dot_stream__executor_dot_dnn__pb2._CONVOLUTIONKIND
_CONVOLUTIONPROTO.fields_by_name['input'].message_type = tensorflow_dot_stream__executor_dot_dnn__pb2._TENSORDESCRIPTORPROTO
_CONVOLUTIONPROTO.fields_by_name['filter'].message_type = tensorflow_dot_stream__executor_dot_dnn__pb2._TENSORDESCRIPTORPROTO
_CONVOLUTIONPROTO.fields_by_name['output'].message_type = tensorflow_dot_stream__executor_dot_dnn__pb2._TENSORDESCRIPTORPROTO
_CONVOLUTIONPROTO.fields_by_name['conv_desc'].message_type = tensorflow_dot_stream__executor_dot_dnn__pb2._CONVOLUTIONDESCRIPTORPROTO
_CONVOLUTIONPROTO.fields_by_name['activation'].enum_type = tensorflow_dot_stream__executor_dot_dnn__pb2._ACTIVATIONMODE
DESCRIPTOR.message_types_by_name['ConvolutionProto'] = _CONVOLUTIONPROTO
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ConvolutionProto = _reflection.GeneratedProtocolMessageType('ConvolutionProto', (_message.Message,), {
  'DESCRIPTOR' : _CONVOLUTIONPROTO,
  '__module__' : 'tensorflow.core.protobuf.conv_autotuning_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.ConvolutionProto)
  })
_sym_db.RegisterMessage(ConvolutionProto)


# @@protoc_insertion_point(module_scope)

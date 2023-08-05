# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/debug/debug_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from pythie_serving.tensorflow_proto.tensorflow.core.framework import tensor_pb2 as tensorflow_dot_core_dot_framework_dot_tensor__pb2
from pythie_serving.tensorflow_proto.tensorflow.core.profiler import tfprof_log_pb2 as tensorflow_dot_core_dot_profiler_dot_tfprof__log__pb2
from pythie_serving.tensorflow_proto.tensorflow.core.protobuf import debug_pb2 as tensorflow_dot_core_dot_protobuf_dot_debug__pb2
from pythie_serving.tensorflow_proto.tensorflow.core.util import event_pb2 as tensorflow_dot_core_dot_util_dot_event__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorflow/core/debug/debug_service.proto',
  package='tensorflow',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n)tensorflow/core/debug/debug_service.proto\x12\ntensorflow\x1a&tensorflow/core/framework/tensor.proto\x1a)tensorflow/core/profiler/tfprof_log.proto\x1a$tensorflow/core/protobuf/debug.proto\x1a tensorflow/core/util/event.proto\"\xde\x02\n\nEventReply\x12I\n\x16\x64\x65\x62ug_op_state_changes\x18\x01 \x03(\x0b\x32).tensorflow.EventReply.DebugOpStateChange\x12\'\n\x06tensor\x18\x02 \x01(\x0b\x32\x17.tensorflow.TensorProto\x1a\xdb\x01\n\x12\x44\x65\x62ugOpStateChange\x12>\n\x05state\x18\x01 \x01(\x0e\x32/.tensorflow.EventReply.DebugOpStateChange.State\x12\x11\n\tnode_name\x18\x02 \x01(\t\x12\x13\n\x0boutput_slot\x18\x03 \x01(\x05\x12\x10\n\x08\x64\x65\x62ug_op\x18\x04 \x01(\t\"K\n\x05State\x12\x15\n\x11STATE_UNSPECIFIED\x10\x00\x12\x0c\n\x08\x44ISABLED\x10\x01\x12\r\n\tREAD_ONLY\x10\x02\x12\x0e\n\nREAD_WRITE\x10\x03\"\xa7\x03\n\rCallTraceback\x12\x35\n\tcall_type\x18\x01 \x01(\x0e\x32\".tensorflow.CallTraceback.CallType\x12\x10\n\x08\x63\x61ll_key\x18\x02 \x01(\t\x12\x30\n\x0corigin_stack\x18\x03 \x01(\x0b\x32\x1a.tensorflow.tfprof.CodeDef\x12L\n\x13origin_id_to_string\x18\x04 \x03(\x0b\x32/.tensorflow.CallTraceback.OriginIdToStringEntry\x12\x36\n\x0fgraph_traceback\x18\x05 \x01(\x0b\x32\x1d.tensorflow.tfprof.OpLogProto\x12\x15\n\rgraph_version\x18\x06 \x01(\x03\x1a\x37\n\x15OriginIdToStringEntry\x12\x0b\n\x03key\x18\x01 \x01(\x03\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"E\n\x08\x43\x61llType\x12\x0f\n\x0bUNSPECIFIED\x10\x00\x12\x13\n\x0fGRAPH_EXECUTION\x10\x01\x12\x13\n\x0f\x45\x41GER_EXECUTION\x10\x02\x32\xdd\x01\n\rEventListener\x12;\n\nSendEvents\x12\x11.tensorflow.Event\x1a\x16.tensorflow.EventReply(\x01\x30\x01\x12\x43\n\x0eSendTracebacks\x12\x19.tensorflow.CallTraceback\x1a\x16.tensorflow.EventReply\x12J\n\x0fSendSourceFiles\x12\x1f.tensorflow.DebuggedSourceFiles\x1a\x16.tensorflow.EventReplyb\x06proto3')
  ,
  dependencies=[tensorflow_dot_core_dot_framework_dot_tensor__pb2.DESCRIPTOR,tensorflow_dot_core_dot_profiler_dot_tfprof__log__pb2.DESCRIPTOR,tensorflow_dot_core_dot_protobuf_dot_debug__pb2.DESCRIPTOR,tensorflow_dot_core_dot_util_dot_event__pb2.DESCRIPTOR,])



_EVENTREPLY_DEBUGOPSTATECHANGE_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='tensorflow.EventReply.DebugOpStateChange.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='STATE_UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DISABLED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='READ_ONLY', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='READ_WRITE', index=3, number=3,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=488,
  serialized_end=563,
)
_sym_db.RegisterEnumDescriptor(_EVENTREPLY_DEBUGOPSTATECHANGE_STATE)

_CALLTRACEBACK_CALLTYPE = _descriptor.EnumDescriptor(
  name='CallType',
  full_name='tensorflow.CallTraceback.CallType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNSPECIFIED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='GRAPH_EXECUTION', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='EAGER_EXECUTION', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=920,
  serialized_end=989,
)
_sym_db.RegisterEnumDescriptor(_CALLTRACEBACK_CALLTYPE)


_EVENTREPLY_DEBUGOPSTATECHANGE = _descriptor.Descriptor(
  name='DebugOpStateChange',
  full_name='tensorflow.EventReply.DebugOpStateChange',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='tensorflow.EventReply.DebugOpStateChange.state', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='node_name', full_name='tensorflow.EventReply.DebugOpStateChange.node_name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='output_slot', full_name='tensorflow.EventReply.DebugOpStateChange.output_slot', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='debug_op', full_name='tensorflow.EventReply.DebugOpStateChange.debug_op', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _EVENTREPLY_DEBUGOPSTATECHANGE_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=344,
  serialized_end=563,
)

_EVENTREPLY = _descriptor.Descriptor(
  name='EventReply',
  full_name='tensorflow.EventReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='debug_op_state_changes', full_name='tensorflow.EventReply.debug_op_state_changes', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tensor', full_name='tensorflow.EventReply.tensor', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_EVENTREPLY_DEBUGOPSTATECHANGE, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=213,
  serialized_end=563,
)


_CALLTRACEBACK_ORIGINIDTOSTRINGENTRY = _descriptor.Descriptor(
  name='OriginIdToStringEntry',
  full_name='tensorflow.CallTraceback.OriginIdToStringEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='tensorflow.CallTraceback.OriginIdToStringEntry.key', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='tensorflow.CallTraceback.OriginIdToStringEntry.value', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=863,
  serialized_end=918,
)

_CALLTRACEBACK = _descriptor.Descriptor(
  name='CallTraceback',
  full_name='tensorflow.CallTraceback',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='call_type', full_name='tensorflow.CallTraceback.call_type', index=0,
      number=1, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='call_key', full_name='tensorflow.CallTraceback.call_key', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='origin_stack', full_name='tensorflow.CallTraceback.origin_stack', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='origin_id_to_string', full_name='tensorflow.CallTraceback.origin_id_to_string', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='graph_traceback', full_name='tensorflow.CallTraceback.graph_traceback', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='graph_version', full_name='tensorflow.CallTraceback.graph_version', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CALLTRACEBACK_ORIGINIDTOSTRINGENTRY, ],
  enum_types=[
    _CALLTRACEBACK_CALLTYPE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=566,
  serialized_end=989,
)

_EVENTREPLY_DEBUGOPSTATECHANGE.fields_by_name['state'].enum_type = _EVENTREPLY_DEBUGOPSTATECHANGE_STATE
_EVENTREPLY_DEBUGOPSTATECHANGE.containing_type = _EVENTREPLY
_EVENTREPLY_DEBUGOPSTATECHANGE_STATE.containing_type = _EVENTREPLY_DEBUGOPSTATECHANGE
_EVENTREPLY.fields_by_name['debug_op_state_changes'].message_type = _EVENTREPLY_DEBUGOPSTATECHANGE
_EVENTREPLY.fields_by_name['tensor'].message_type = tensorflow_dot_core_dot_framework_dot_tensor__pb2._TENSORPROTO
_CALLTRACEBACK_ORIGINIDTOSTRINGENTRY.containing_type = _CALLTRACEBACK
_CALLTRACEBACK.fields_by_name['call_type'].enum_type = _CALLTRACEBACK_CALLTYPE
_CALLTRACEBACK.fields_by_name['origin_stack'].message_type = tensorflow_dot_core_dot_profiler_dot_tfprof__log__pb2._CODEDEF
_CALLTRACEBACK.fields_by_name['origin_id_to_string'].message_type = _CALLTRACEBACK_ORIGINIDTOSTRINGENTRY
_CALLTRACEBACK.fields_by_name['graph_traceback'].message_type = tensorflow_dot_core_dot_profiler_dot_tfprof__log__pb2._OPLOGPROTO
_CALLTRACEBACK_CALLTYPE.containing_type = _CALLTRACEBACK
DESCRIPTOR.message_types_by_name['EventReply'] = _EVENTREPLY
DESCRIPTOR.message_types_by_name['CallTraceback'] = _CALLTRACEBACK
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

EventReply = _reflection.GeneratedProtocolMessageType('EventReply', (_message.Message,), {

  'DebugOpStateChange' : _reflection.GeneratedProtocolMessageType('DebugOpStateChange', (_message.Message,), {
    'DESCRIPTOR' : _EVENTREPLY_DEBUGOPSTATECHANGE,
    '__module__' : 'tensorflow.core.debug.debug_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.EventReply.DebugOpStateChange)
    })
  ,
  'DESCRIPTOR' : _EVENTREPLY,
  '__module__' : 'tensorflow.core.debug.debug_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.EventReply)
  })
_sym_db.RegisterMessage(EventReply)
_sym_db.RegisterMessage(EventReply.DebugOpStateChange)

CallTraceback = _reflection.GeneratedProtocolMessageType('CallTraceback', (_message.Message,), {

  'OriginIdToStringEntry' : _reflection.GeneratedProtocolMessageType('OriginIdToStringEntry', (_message.Message,), {
    'DESCRIPTOR' : _CALLTRACEBACK_ORIGINIDTOSTRINGENTRY,
    '__module__' : 'tensorflow.core.debug.debug_service_pb2'
    # @@protoc_insertion_point(class_scope:tensorflow.CallTraceback.OriginIdToStringEntry)
    })
  ,
  'DESCRIPTOR' : _CALLTRACEBACK,
  '__module__' : 'tensorflow.core.debug.debug_service_pb2'
  # @@protoc_insertion_point(class_scope:tensorflow.CallTraceback)
  })
_sym_db.RegisterMessage(CallTraceback)
_sym_db.RegisterMessage(CallTraceback.OriginIdToStringEntry)


_CALLTRACEBACK_ORIGINIDTOSTRINGENTRY._options = None

_EVENTLISTENER = _descriptor.ServiceDescriptor(
  name='EventListener',
  full_name='tensorflow.EventListener',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=992,
  serialized_end=1213,
  methods=[
  _descriptor.MethodDescriptor(
    name='SendEvents',
    full_name='tensorflow.EventListener.SendEvents',
    index=0,
    containing_service=None,
    input_type=tensorflow_dot_core_dot_util_dot_event__pb2._EVENT,
    output_type=_EVENTREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendTracebacks',
    full_name='tensorflow.EventListener.SendTracebacks',
    index=1,
    containing_service=None,
    input_type=_CALLTRACEBACK,
    output_type=_EVENTREPLY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='SendSourceFiles',
    full_name='tensorflow.EventListener.SendSourceFiles',
    index=2,
    containing_service=None,
    input_type=tensorflow_dot_core_dot_protobuf_dot_debug__pb2._DEBUGGEDSOURCEFILES,
    output_type=_EVENTREPLY,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_EVENTLISTENER)

DESCRIPTOR.services_by_name['EventListener'] = _EVENTLISTENER

# @@protoc_insertion_point(module_scope)

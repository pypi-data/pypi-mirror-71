# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: codemao_observefallclimb.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='codemao_observefallclimb.proto',
    package='',
    syntax='proto3',
    serialized_options=b'\n\025com.ubtechinc.codemao',
    serialized_pb=b'\n\x1e\x63odemao_observefallclimb.proto\".\n\x17ObserveFallClimbRequest\x12\x13\n\x0bisSubscribe\x18\x01 \x01(\x08\"*\n\x18ObserveFallClimbResponse\x12\x0e\n\x06status\x18\x01 \x01(\x05\x42\x17\n\x15\x63om.ubtechinc.codemaob\x06proto3'
)

_OBSERVEFALLCLIMBREQUEST = _descriptor.Descriptor(
    name='ObserveFallClimbRequest',
    full_name='ObserveFallClimbRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='isSubscribe', full_name='ObserveFallClimbRequest.isSubscribe', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
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
    serialized_start=34,
    serialized_end=80,
)

_OBSERVEFALLCLIMBRESPONSE = _descriptor.Descriptor(
    name='ObserveFallClimbResponse',
    full_name='ObserveFallClimbResponse',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='status', full_name='ObserveFallClimbResponse.status', index=0,
            number=1, type=5, cpp_type=1, label=1,
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
    serialized_start=82,
    serialized_end=124,
)

DESCRIPTOR.message_types_by_name['ObserveFallClimbRequest'] = _OBSERVEFALLCLIMBREQUEST
DESCRIPTOR.message_types_by_name['ObserveFallClimbResponse'] = _OBSERVEFALLCLIMBRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObserveFallClimbRequest = _reflection.GeneratedProtocolMessageType('ObserveFallClimbRequest', (_message.Message,), {
    'DESCRIPTOR': _OBSERVEFALLCLIMBREQUEST,
    '__module__': 'codemao_observefallclimb_pb2'
    # @@protoc_insertion_point(class_scope:ObserveFallClimbRequest)
})
_sym_db.RegisterMessage(ObserveFallClimbRequest)

ObserveFallClimbResponse = _reflection.GeneratedProtocolMessageType('ObserveFallClimbResponse', (_message.Message,), {
    'DESCRIPTOR': _OBSERVEFALLCLIMBRESPONSE,
    '__module__': 'codemao_observefallclimb_pb2'
    # @@protoc_insertion_point(class_scope:ObserveFallClimbResponse)
})
_sym_db.RegisterMessage(ObserveFallClimbResponse)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: codemao_observeheadracket.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='codemao_observeheadracket.proto',
    package='',
    syntax='proto3',
    serialized_options=b'\n\025com.ubtechinc.codemao',
    serialized_pb=b'\n\x1f\x63odemao_observeheadracket.proto\"/\n\x18ObserveHeadRacketRequest\x12\x13\n\x0bisSubscribe\x18\x01 \x01(\x08\")\n\x19ObserveHeadRacketResponse\x12\x0c\n\x04type\x18\x01 \x01(\x05\x42\x17\n\x15\x63om.ubtechinc.codemaob\x06proto3'
)

_OBSERVEHEADRACKETREQUEST = _descriptor.Descriptor(
    name='ObserveHeadRacketRequest',
    full_name='ObserveHeadRacketRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='isSubscribe', full_name='ObserveHeadRacketRequest.isSubscribe', index=0,
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
    serialized_start=35,
    serialized_end=82,
)

_OBSERVEHEADRACKETRESPONSE = _descriptor.Descriptor(
    name='ObserveHeadRacketResponse',
    full_name='ObserveHeadRacketResponse',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='type', full_name='ObserveHeadRacketResponse.type', index=0,
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
    serialized_start=84,
    serialized_end=125,
)

DESCRIPTOR.message_types_by_name['ObserveHeadRacketRequest'] = _OBSERVEHEADRACKETREQUEST
DESCRIPTOR.message_types_by_name['ObserveHeadRacketResponse'] = _OBSERVEHEADRACKETRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ObserveHeadRacketRequest = _reflection.GeneratedProtocolMessageType('ObserveHeadRacketRequest', (_message.Message,), {
    'DESCRIPTOR': _OBSERVEHEADRACKETREQUEST,
    '__module__': 'codemao_observeheadracket_pb2'
    # @@protoc_insertion_point(class_scope:ObserveHeadRacketRequest)
})
_sym_db.RegisterMessage(ObserveHeadRacketRequest)

ObserveHeadRacketResponse = _reflection.GeneratedProtocolMessageType('ObserveHeadRacketResponse', (_message.Message,), {
    'DESCRIPTOR': _OBSERVEHEADRACKETRESPONSE,
    '__module__': 'codemao_observeheadracket_pb2'
    # @@protoc_insertion_point(class_scope:ObserveHeadRacketResponse)
})
_sym_db.RegisterMessage(ObserveHeadRacketResponse)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

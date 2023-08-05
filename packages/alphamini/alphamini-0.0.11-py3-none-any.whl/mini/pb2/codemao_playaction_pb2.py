# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: codemao_playaction.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='codemao_playaction.proto',
    package='',
    syntax='proto3',
    serialized_options=b'\n\025com.ubtechinc.codemao',
    serialized_pb=b'\n\x18\x63odemao_playaction.proto\"\'\n\x11PlayActionRequest\x12\x12\n\nactionName\x18\x01 \x01(\t\";\n\x12PlayActionResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x12\n\nresultCode\x18\x02 \x01(\x05\x42\x17\n\x15\x63om.ubtechinc.codemaob\x06proto3'
)

_PLAYACTIONREQUEST = _descriptor.Descriptor(
    name='PlayActionRequest',
    full_name='PlayActionRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='actionName', full_name='PlayActionRequest.actionName', index=0,
            number=1, type=9, cpp_type=9, label=1,
            has_default_value=False, default_value=b"".decode('utf-8'),
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
    serialized_start=28,
    serialized_end=67,
)

_PLAYACTIONRESPONSE = _descriptor.Descriptor(
    name='PlayActionResponse',
    full_name='PlayActionResponse',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='isSuccess', full_name='PlayActionResponse.isSuccess', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='resultCode', full_name='PlayActionResponse.resultCode', index=1,
            number=2, type=5, cpp_type=1, label=1,
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
    serialized_start=69,
    serialized_end=128,
)

DESCRIPTOR.message_types_by_name['PlayActionRequest'] = _PLAYACTIONREQUEST
DESCRIPTOR.message_types_by_name['PlayActionResponse'] = _PLAYACTIONRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

PlayActionRequest = _reflection.GeneratedProtocolMessageType('PlayActionRequest', (_message.Message,), {
    'DESCRIPTOR': _PLAYACTIONREQUEST,
    '__module__': 'codemao_playaction_pb2'
    # @@protoc_insertion_point(class_scope:PlayActionRequest)
})
_sym_db.RegisterMessage(PlayActionRequest)

PlayActionResponse = _reflection.GeneratedProtocolMessageType('PlayActionResponse', (_message.Message,), {
    'DESCRIPTOR': _PLAYACTIONRESPONSE,
    '__module__': 'codemao_playaction_pb2'
    # @@protoc_insertion_point(class_scope:PlayActionResponse)
})
_sym_db.RegisterMessage(PlayActionResponse)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

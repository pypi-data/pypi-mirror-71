# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: codemao_revertorigin.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='codemao_revertorigin.proto',
    package='',
    syntax='proto3',
    serialized_options=b'\n\025com.ubtechinc.codemao',
    serialized_pb=b'\n\x1a\x63odemao_revertorigin.proto\"\x15\n\x13RevertOriginRequest\"=\n\x14RevertOriginResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x12\n\nresultCode\x18\x02 \x01(\x05\x42\x17\n\x15\x63om.ubtechinc.codemaob\x06proto3'
)

_REVERTORIGINREQUEST = _descriptor.Descriptor(
    name='RevertOriginRequest',
    full_name='RevertOriginRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
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
    serialized_start=30,
    serialized_end=51,
)

_REVERTORIGINRESPONSE = _descriptor.Descriptor(
    name='RevertOriginResponse',
    full_name='RevertOriginResponse',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='isSuccess', full_name='RevertOriginResponse.isSuccess', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='resultCode', full_name='RevertOriginResponse.resultCode', index=1,
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
    serialized_start=53,
    serialized_end=114,
)

DESCRIPTOR.message_types_by_name['RevertOriginRequest'] = _REVERTORIGINREQUEST
DESCRIPTOR.message_types_by_name['RevertOriginResponse'] = _REVERTORIGINRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RevertOriginRequest = _reflection.GeneratedProtocolMessageType('RevertOriginRequest', (_message.Message,), {
    'DESCRIPTOR': _REVERTORIGINREQUEST,
    '__module__': 'codemao_revertorigin_pb2'
    # @@protoc_insertion_point(class_scope:RevertOriginRequest)
})
_sym_db.RegisterMessage(RevertOriginRequest)

RevertOriginResponse = _reflection.GeneratedProtocolMessageType('RevertOriginResponse', (_message.Message,), {
    'DESCRIPTOR': _REVERTORIGINRESPONSE,
    '__module__': 'codemao_revertorigin_pb2'
    # @@protoc_insertion_point(class_scope:RevertOriginResponse)
})
_sym_db.RegisterMessage(RevertOriginResponse)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

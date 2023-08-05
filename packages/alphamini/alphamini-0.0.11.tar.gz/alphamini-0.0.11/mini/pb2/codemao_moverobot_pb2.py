# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: codemao_moverobot.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor.FileDescriptor(
    name='codemao_moverobot.proto',
    package='',
    syntax='proto3',
    serialized_options=b'\n\025com.ubtechinc.codemao',
    serialized_pb=b'\n\x17\x63odemao_moverobot.proto\"3\n\x10MoveRobotRequest\x12\x11\n\tdirection\x18\x01 \x01(\x05\x12\x0c\n\x04step\x18\x02 \x01(\x05\"4\n\x11MoveRobotResponse\x12\x11\n\tisSuccess\x18\x01 \x01(\x08\x12\x0c\n\x04\x63ode\x18\x02 \x01(\x05\x42\x17\n\x15\x63om.ubtechinc.codemaob\x06proto3'
)

_MOVEROBOTREQUEST = _descriptor.Descriptor(
    name='MoveRobotRequest',
    full_name='MoveRobotRequest',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='direction', full_name='MoveRobotRequest.direction', index=0,
            number=1, type=5, cpp_type=1, label=1,
            has_default_value=False, default_value=0,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='step', full_name='MoveRobotRequest.step', index=1,
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
    serialized_start=27,
    serialized_end=78,
)

_MOVEROBOTRESPONSE = _descriptor.Descriptor(
    name='MoveRobotResponse',
    full_name='MoveRobotResponse',
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name='isSuccess', full_name='MoveRobotResponse.isSuccess', index=0,
            number=1, type=8, cpp_type=7, label=1,
            has_default_value=False, default_value=False,
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            serialized_options=None, file=DESCRIPTOR),
        _descriptor.FieldDescriptor(
            name='code', full_name='MoveRobotResponse.code', index=1,
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
    serialized_start=80,
    serialized_end=132,
)

DESCRIPTOR.message_types_by_name['MoveRobotRequest'] = _MOVEROBOTREQUEST
DESCRIPTOR.message_types_by_name['MoveRobotResponse'] = _MOVEROBOTRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

MoveRobotRequest = _reflection.GeneratedProtocolMessageType('MoveRobotRequest', (_message.Message,), {
    'DESCRIPTOR': _MOVEROBOTREQUEST,
    '__module__': 'codemao_moverobot_pb2'
    # @@protoc_insertion_point(class_scope:MoveRobotRequest)
})
_sym_db.RegisterMessage(MoveRobotRequest)

MoveRobotResponse = _reflection.GeneratedProtocolMessageType('MoveRobotResponse', (_message.Message,), {
    'DESCRIPTOR': _MOVEROBOTRESPONSE,
    '__module__': 'codemao_moverobot_pb2'
    # @@protoc_insertion_point(class_scope:MoveRobotResponse)
})
_sym_db.RegisterMessage(MoveRobotResponse)

DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)

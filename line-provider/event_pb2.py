# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: event.proto
# Protobuf Python Version: 5.28.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC, 5, 28, 1, "", "event.proto"
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x0b\x65vent.proto\x12\x05\x65vent"\t\n\x07Request"\x1f\n\x0bRequestById\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t"O\n\x05\x45vent\x12\x10\n\x08\x65vent_id\x18\x01 \x01(\t\x12\x13\n\x0b\x63oefficient\x18\x02 \x01(\t\x12\x10\n\x08\x64\x65\x61\x64line\x18\x03 \x01(\t\x12\r\n\x05state\x18\x04 \x01(\t"(\n\x08Response\x12\x1c\n\x06\x65vents\x18\x01 \x03(\x0b\x32\x0c.event.Event"\x1e\n\rResponseCheck\x12\r\n\x05\x63heck\x18\x01 \x01(\x08\x32\xdc\x01\n\x0c\x45ventService\x12.\n\x0bGetEventAll\x12\x0e.event.Request\x1a\x0f.event.Response\x12+\n\x08GetEvent\x12\x0e.event.Request\x1a\x0f.event.Response\x12\x33\n\x0cGetEventById\x12\x12.event.RequestById\x1a\x0f.event.Response\x12:\n\x0e\x45ventCheckTime\x12\x12.event.RequestById\x1a\x14.event.ResponseCheckb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "event_pb2", _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals["_REQUEST"]._serialized_start = 22
    _globals["_REQUEST"]._serialized_end = 31
    _globals["_REQUESTBYID"]._serialized_start = 33
    _globals["_REQUESTBYID"]._serialized_end = 64
    _globals["_EVENT"]._serialized_start = 66
    _globals["_EVENT"]._serialized_end = 145
    _globals["_RESPONSE"]._serialized_start = 147
    _globals["_RESPONSE"]._serialized_end = 187
    _globals["_RESPONSECHECK"]._serialized_start = 189
    _globals["_RESPONSECHECK"]._serialized_end = 219
    _globals["_EVENTSERVICE"]._serialized_start = 222
    _globals["_EVENTSERVICE"]._serialized_end = 442
# @@protoc_insertion_point(module_scope)
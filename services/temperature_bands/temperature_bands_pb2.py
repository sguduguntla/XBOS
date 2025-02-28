# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: temperature_bands.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='temperature_bands.proto',
  package='schedules_historical',
  syntax='proto3',
  serialized_pb=_b('\n\x17temperature_bands.proto\x12\x14schedules_historical\"c\n\x07Request\x12\x10\n\x08\x62uilding\x18\x01 \x01(\t\x12\x0c\n\x04zone\x18\x02 \x01(\t\x12\r\n\x05start\x18\x03 \x01(\x03\x12\x0b\n\x03\x65nd\x18\x04 \x01(\x03\x12\x0e\n\x06window\x18\x05 \x01(\t\x12\x0c\n\x04unit\x18\x06 \x01(\t\"^\n\rSchedulePoint\x12\x0c\n\x04time\x18\x01 \x01(\x03\x12\x17\n\x0ftemperature_low\x18\x02 \x01(\x01\x12\x18\n\x10temperature_high\x18\x03 \x01(\x01\x12\x0c\n\x04unit\x18\x04 \x01(\t\"G\n\rScheduleReply\x12\x36\n\tschedules\x18\x01 \x03(\x0b\x32#.schedules_historical.SchedulePoint2\xbb\x01\n\tSchedules\x12V\n\x0eGetComfortband\x12\x1d.schedules_historical.Request\x1a#.schedules_historical.ScheduleReply\"\x00\x12V\n\x0eGetDoNotExceed\x12\x1d.schedules_historical.Request\x1a#.schedules_historical.ScheduleReply\"\x00\x42\x02P\x01\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='schedules_historical.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='building', full_name='schedules_historical.Request.building', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone', full_name='schedules_historical.Request.zone', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='start', full_name='schedules_historical.Request.start', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='end', full_name='schedules_historical.Request.end', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='window', full_name='schedules_historical.Request.window', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='schedules_historical.Request.unit', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=49,
  serialized_end=148,
)


_SCHEDULEPOINT = _descriptor.Descriptor(
  name='SchedulePoint',
  full_name='schedules_historical.SchedulePoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time', full_name='schedules_historical.SchedulePoint.time', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature_low', full_name='schedules_historical.SchedulePoint.temperature_low', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature_high', full_name='schedules_historical.SchedulePoint.temperature_high', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='schedules_historical.SchedulePoint.unit', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=150,
  serialized_end=244,
)


_SCHEDULEREPLY = _descriptor.Descriptor(
  name='ScheduleReply',
  full_name='schedules_historical.ScheduleReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='schedules', full_name='schedules_historical.ScheduleReply.schedules', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=246,
  serialized_end=317,
)

_SCHEDULEREPLY.fields_by_name['schedules'].message_type = _SCHEDULEPOINT
DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['SchedulePoint'] = _SCHEDULEPOINT
DESCRIPTOR.message_types_by_name['ScheduleReply'] = _SCHEDULEREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'temperature_bands_pb2'
  # @@protoc_insertion_point(class_scope:schedules_historical.Request)
  ))
_sym_db.RegisterMessage(Request)

SchedulePoint = _reflection.GeneratedProtocolMessageType('SchedulePoint', (_message.Message,), dict(
  DESCRIPTOR = _SCHEDULEPOINT,
  __module__ = 'temperature_bands_pb2'
  # @@protoc_insertion_point(class_scope:schedules_historical.SchedulePoint)
  ))
_sym_db.RegisterMessage(SchedulePoint)

ScheduleReply = _reflection.GeneratedProtocolMessageType('ScheduleReply', (_message.Message,), dict(
  DESCRIPTOR = _SCHEDULEREPLY,
  __module__ = 'temperature_bands_pb2'
  # @@protoc_insertion_point(class_scope:schedules_historical.ScheduleReply)
  ))
_sym_db.RegisterMessage(ScheduleReply)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('P\001'))

_SCHEDULES = _descriptor.ServiceDescriptor(
  name='Schedules',
  full_name='schedules_historical.Schedules',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=320,
  serialized_end=507,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetComfortband',
    full_name='schedules_historical.Schedules.GetComfortband',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_SCHEDULEREPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='GetDoNotExceed',
    full_name='schedules_historical.Schedules.GetDoNotExceed',
    index=1,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_SCHEDULEREPLY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SCHEDULES)

DESCRIPTOR.services_by_name['Schedules'] = _SCHEDULES

# @@protoc_insertion_point(module_scope)

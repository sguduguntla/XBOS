# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: hvac_consumption.proto

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
  name='hvac_consumption.proto',
  package='hvac_consumption',
  syntax='proto3',
  serialized_pb=_b('\n\x16hvac_consumption.proto\x12\x10hvac_consumption\")\n\x07Request\x12\x10\n\x08\x62uilding\x18\x01 \x01(\t\x12\x0c\n\x04zone\x18\x02 \x01(\t\"\xc9\x01\n\x10\x43onsumptionPoint\x12\x1b\n\x13heating_consumption\x18\x01 \x01(\x01\x12\x1b\n\x13\x63ooling_consumption\x18\x02 \x01(\x01\x12\x1f\n\x17ventilation_consumption\x18\x03 \x01(\x01\x12%\n\x1dheating_consumption_stage_two\x18\x04 \x01(\x01\x12%\n\x1d\x63ooling_consumption_stage_two\x18\x05 \x01(\x01\x12\x0c\n\x04unit\x18\x06 \x01(\t2d\n\x0f\x43onsumptionHVAC\x12Q\n\x0eGetConsumption\x12\x19.hvac_consumption.Request\x1a\".hvac_consumption.ConsumptionPoint\"\x00\x42\x02P\x01\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='hvac_consumption.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='building', full_name='hvac_consumption.Request.building', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='zone', full_name='hvac_consumption.Request.zone', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=44,
  serialized_end=85,
)


_CONSUMPTIONPOINT = _descriptor.Descriptor(
  name='ConsumptionPoint',
  full_name='hvac_consumption.ConsumptionPoint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='heating_consumption', full_name='hvac_consumption.ConsumptionPoint.heating_consumption', index=0,
      number=1, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cooling_consumption', full_name='hvac_consumption.ConsumptionPoint.cooling_consumption', index=1,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='ventilation_consumption', full_name='hvac_consumption.ConsumptionPoint.ventilation_consumption', index=2,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='heating_consumption_stage_two', full_name='hvac_consumption.ConsumptionPoint.heating_consumption_stage_two', index=3,
      number=4, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='cooling_consumption_stage_two', full_name='hvac_consumption.ConsumptionPoint.cooling_consumption_stage_two', index=4,
      number=5, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='unit', full_name='hvac_consumption.ConsumptionPoint.unit', index=5,
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
  serialized_start=88,
  serialized_end=289,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['ConsumptionPoint'] = _CONSUMPTIONPOINT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'hvac_consumption_pb2'
  # @@protoc_insertion_point(class_scope:hvac_consumption.Request)
  ))
_sym_db.RegisterMessage(Request)

ConsumptionPoint = _reflection.GeneratedProtocolMessageType('ConsumptionPoint', (_message.Message,), dict(
  DESCRIPTOR = _CONSUMPTIONPOINT,
  __module__ = 'hvac_consumption_pb2'
  # @@protoc_insertion_point(class_scope:hvac_consumption.ConsumptionPoint)
  ))
_sym_db.RegisterMessage(ConsumptionPoint)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('P\001'))

_CONSUMPTIONHVAC = _descriptor.ServiceDescriptor(
  name='ConsumptionHVAC',
  full_name='hvac_consumption.ConsumptionHVAC',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=291,
  serialized_end=391,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetConsumption',
    full_name='hvac_consumption.ConsumptionHVAC.GetConsumption',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_CONSUMPTIONPOINT,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_CONSUMPTIONHVAC)

DESCRIPTOR.services_by_name['ConsumptionHVAC'] = _CONSUMPTIONHVAC

# @@protoc_insertion_point(module_scope)

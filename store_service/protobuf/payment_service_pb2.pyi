from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PaymentStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PAYMENT_STATUS_UNSPECIFIED: _ClassVar[PaymentStatus]
    PAYMENT_STATUS_PENDING: _ClassVar[PaymentStatus]
    PAYMENT_STATUS_SUCCEEDED: _ClassVar[PaymentStatus]
    PAYMENT_STATUS_FAILED: _ClassVar[PaymentStatus]
PAYMENT_STATUS_UNSPECIFIED: PaymentStatus
PAYMENT_STATUS_PENDING: PaymentStatus
PAYMENT_STATUS_SUCCEEDED: PaymentStatus
PAYMENT_STATUS_FAILED: PaymentStatus

class PaymentRequest(_message.Message):
    __slots__ = ("user_id", "appid")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    APPID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    appid: str
    def __init__(self, user_id: _Optional[str] = ..., appid: _Optional[str] = ...) -> None: ...

class PaymentResponse(_message.Message):
    __slots__ = ("user_id", "status")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    status: PaymentStatus
    def __init__(self, user_id: _Optional[str] = ..., status: _Optional[_Union[PaymentStatus, str]] = ...) -> None: ...

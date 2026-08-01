from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddGameToUserRequest(_message.Message):
    __slots__ = ("user_id", "game_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    game_id: str
    def __init__(self, user_id: _Optional[str] = ..., game_id: _Optional[str] = ...) -> None: ...

class AddGameToUserResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class HasGameRequest(_message.Message):
    __slots__ = ("user_id", "game_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    GAME_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    game_id: str
    def __init__(self, user_id: _Optional[str] = ..., game_id: _Optional[str] = ...) -> None: ...

class HasGameResponse(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: _Optional[bool] = ...) -> None: ...

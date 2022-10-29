import typing as t

from pydantic import BaseModel as _model


class BaseUserScheme(_model):
    username: str
    firstname: str
    lastname: t.Optional[str]

    class Config:
        orm_mode: bool = True


class UserScheme(BaseUserScheme):
    id: int

import sqlalchemy as _sql
from .base import db


class UserModel(db.base):
    __tablename__: str = 'users'
    id: _sql.Column = _sql.Column(
        "id",
        _sql.BigInteger,
        primary_key=True,
        nullable=False,
        index=True,
    )
    username: _sql.Column = _sql.Column(
        "username",
        _sql.String(32),
        unique=True,
        nullable=False,
        index=True,
    )
    firstname: _sql.Column = _sql.Column(
        "firstname",
        _sql.String(64),
        nullable=False,
    )
    lastname: _sql.Column = _sql.Column(
        "lastname",
        _sql.String(64),
        nullable=True
    )

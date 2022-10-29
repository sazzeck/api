import logging

import sqlalchemy.ext.asyncio as _asql
from sqlalchemy import orm as _orm
from sqlalchemy.ext import declarative as _declarative

from ..utils import Config as _config
from ..utils import SingletonMeta


class Session:

    __slots__: tuple[str] = "_async_session"

    def __init__(self, engine) -> None:
        self._async_session: _asql.AsyncSession = _orm.sessionmaker(
            bind=engine,
            expire_on_commit=False,
            class_=_asql.AsyncSession,
        )

    async def get_session(self) -> _asql.AsyncSession:
        async with self._async_session() as session:
            try:
                yield session
            except Exception:
                await session.rollback()


class DataBase(metaclass=SingletonMeta):

    __slots__: tuple[str] = ("base", "_engine", "session", "log")

    def __init__(self) -> None:
        self.base = _declarative.declarative_base()
        self._engine: _asql.AsyncEngine = _asql.create_async_engine(
            self._get_url(),
            echo=False,
        )
        self.session: Session = Session(engine=self._engine)
        self.log: logging.Logger = logging.getLogger("DataBase")

    def _get_url(self) -> str:
        url: str = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
            _config.DB_USER,
            _config.DB_PASSWORD,
            _config.DB_HOST,
            _config.DB_PORT,
            _config.DB_NAME,
        )
        return url

    async def create_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(self.base.metadata.create_all)

    async def reset_tables(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(self.base.metadata.drop_all)
            await conn.run_sync(self.base.metadata.create_all)

    async def start_up(self, reset_tables: bool = False) -> None:
        if not reset_tables:
            await self.create_tables()
        else:
            await self.reset_tables()


db: DataBase = DataBase()

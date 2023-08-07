from datetime import datetime
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase)
from sqlalchemy import (
    Boolean, DateTime, ForeignKey, Integer, String)
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from app.models.models import (
    Roles,
    MAX_LEN_EMAIL, MAX_LEN_NAME, MAX_LEN_PASS, MAX_LEN_USERNAME)

DATABASE_URL = (
    'postgresql+asyncpg://'
    f'{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(
        String(length=MAX_LEN_EMAIL),
        index=True,
        nullable=False,
        unique=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=MAX_LEN_PASS),
        nullable=False)
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False)
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False)
    name_first: Mapped[str] = mapped_column(
        String(length=MAX_LEN_NAME))
    name_second: Mapped[str] = mapped_column(
        String(length=MAX_LEN_NAME))
    registered_at: Mapped[DateTime] = mapped_column(
        DateTime,
        default=datetime.utcnow)
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(Roles.id))
    username: Mapped[str] = mapped_column(
        String(length=MAX_LEN_USERNAME),
        index=True,
        nullable=False,
        unique=True)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


# Alembic will be in charge, no need to use:
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

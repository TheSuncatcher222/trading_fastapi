from datetime import datetime
from sqlalchemy import (
    MetaData,
    Column, Table,
    ForeignKey, Integer, JSON, String, TIMESTAMP)

metadata: MetaData = MetaData()

roles: Table = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('permissions', JSON),)

users: Table = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('name_first', String, nullable=False),
    Column('name_second', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('username', String, nullable=False),)

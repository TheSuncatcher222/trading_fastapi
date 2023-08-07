from datetime import datetime
from re import match

from fastapi import HTTPException, status
from sqlalchemy import (
    MetaData,
    CheckConstraint,
    Column,
    Boolean, ForeignKey, Integer, JSON, String, DateTime)
from sqlalchemy.orm import declarative_base, validates

Base = declarative_base()
metadata: MetaData = MetaData()

INVALID_TEXT: str = (
    "Invalid {field} format! Expected {value} with: \n"
    "- latin letters (a-z or A-Z);\n"
    "- numbers (0-9);\n"
    "- dots (.);\n"
    "- underscore (_);\n"
    "- hyphen (-).")
INVALID_EMAIL: str = INVALID_TEXT.format(
    field='email', value='example_email@email.com')
INVALID_USERNAME: str = INVALID_TEXT.format(
    field='username', value='example_username')
PATTERN_EMAIL: str = r'^[a-zA-Z0-9._-]+@[a-z]+\.[a-z]+$'
PATTERN_USERNAME: str = r'^[a-zA-Z0-9._-]+$'

ROLE_NAMES: list[str] = ['bronze', 'silver', 'gold', 'platinum']
INVALID_ROLE_NAME: str = (
    f"Invalid role name! Expected values are {', '.join(ROLE_NAMES)}.")

MAX_LEN_EMAIL: int = 150
MAX_LEN_PASS: int = 1024
MAX_LEN_NAME: int = 50
MAX_LEN_USERNAME: int = 100


class Roles(Base):
    """
    Class represents model for roles.

    Attributes:
        - id: int
            - role's id
            - table's primary key
        - name: str
            - role's name
            - required
            - unique
            - should match any of valid role names ("ROLE_NAMES")
        - permissions: JSON
            - role's list of permissions
    """
    __tablename__ = 'roles'
    metadata = metadata
    id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    permissions = Column(JSON())

    __table_args__ = (
        CheckConstraint(
            name.in_(ROLE_NAMES), name="valid_role_name_constraint"),)


# In PostgreSQL "user" is a reserved keyword, so in our DB we'll use plural
class Users(Base):
    """
    Class represents model for users.

    Attributes:
        - email: str
            - user's email
            - required
            - unique
            - should match (a-z)(A-Z)(.)(-)(_)@(a-z).[a-z] pattern
            - max length is 150 chars
            - indexed
        - hashed_password: str
            - user's password
            - required
        - id: int
            - user's id
            - table's primary key
        - is_active: bool
            - represent user's account activation state
            - default value is "False"
        - is_superuser: bool
            - represent user's admin state
            - default value is "False"
        - is_verified: bool
            - represent user's personal data verification state
            - default value is "False"
        - name_first: str
            - user's first name
            - max length is 50 chars
        - name_second: str
            - user's second name
            - max length is 50 chars
        - registered_at: datetime
            - user's registry moment date and time
            - max length is 50 chars
        - role_id: int
            - user's cite role (see "Roles" class/table)
            - foreign key related to "Roles" class/table
        - username: str
            - user's username
            - required
            - unique
            - should match r'^[a-zA-Z0-9._-]+'
            - max length is 100 chars
            - indexed
    """
    __tablename__ = 'users'
    metadata = metadata

    email = Column(
        String(MAX_LEN_EMAIL), index=True, nullable=False, unique=True)
    hashed_password = Column(String(MAX_LEN_PASS), nullable=False)
    id = Column(Integer(), primary_key=True)
    is_active = Column(Boolean(), default=False)
    is_superuser = Column(Boolean(), default=False)
    is_verified = Column(Boolean(), default=False)
    name_first = Column(String(MAX_LEN_NAME))
    name_second = Column(String(MAX_LEN_NAME))
    registered_at = Column(DateTime(), default=datetime.utcnow)
    role_id = Column(Integer(), ForeignKey('roles.id'))
    username = Column(
        String(MAX_LEN_USERNAME), index=True, nullable=False, unique=True)

    @validates('email')
    def validate_email(self, email):
        """
        Validate the "email" [str] field using a regular expression.
        Returns the validated email if it passes validation [str].
        Raises "ValueError" if the email does not match the pattern.
        """
        if not match(PATTERN_EMAIL, email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=INVALID_EMAIL)
        return email

    @validates('username')
    def validate_username(self, username):
        """
        Validate the "username" [str] field using a regular expression.
        Returns the validated username if it passes validation [str].
        Raises "ValueError" if the username does not match the pattern.
        """
        if not match(PATTERN_USERNAME, username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=INVALID_USERNAME)
        return username

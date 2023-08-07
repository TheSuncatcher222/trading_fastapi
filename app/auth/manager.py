from typing import Optional

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, IntegerIDMixin,
    exceptions, models, schemas)

from app.core.config import SECRET_MANAGER_RESET, SECRET_MANAGER_VERIFICATION
from app.auth.users import User, get_user_db

# Default role id should be for 'Bronze' role, 1 is default.
ROLE_ID_DEFAULT: int = 1


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_MANAGER_RESET
    verification_token_secret = SECRET_MANAGER_VERIFICATION

    async def on_after_register(
            self, user: User, request: Optional[Request] = None):
        print(f'User {user.id} has registered.')

    async def on_after_forgot_password(
            self, user: User, token: str, request: Optional[Request] = None):
        print(f'User {user.id} has forgot their password. '
              f'Reset token: {token}')

    async def on_after_request_verify(
            self, user: User, token: str, request: Optional[Request] = None):
        print(f'Verification requested for user {user.id}. '
              f'Verification token: {token}')

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        """
        Modify fastapi_users.BaseUserManager.create!

        Create a user in database and assigns role with id=1 ('Bronze') to it.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop('password')
        user_dict['hashed_password'] = self.password_helper.hash(password)
        # Update original func with 1 row below:
        user_dict['role_id'] = ROLE_ID_DEFAULT
        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)

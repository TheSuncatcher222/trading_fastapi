from fastapi_users.authentication import (
    AuthenticationBackend, CookieTransport, JWTStrategy)

from app.core.config import SECRET_JWT

ONE_DAY_SEC: int = 24 * 60 * 60

cookie_transport: CookieTransport = CookieTransport(
    cookie_name='auth_cookie',
    cookie_max_age=ONE_DAY_SEC)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        algorithm="HS256",
        secret=SECRET_JWT,
        lifetime_seconds=ONE_DAY_SEC)


auth_backend: AuthenticationBackend = AuthenticationBackend(
    name='jwt',
    transport=cookie_transport,
    get_strategy=get_jwt_strategy)

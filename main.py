from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from core import SEND_DEBUG
from models import Trades, Users
from test_db import test_users, test_trades

app: FastAPI = FastAPI(title='Trading FastAPI App')


if SEND_DEBUG:
    @app.exception_handler(ValidationException)
    async def validation_exception_handler(
            request: Request, exc: ValidationException):
        print(exc.errors())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({"detail": exc.errors()}))


@app.get('/')
def say_hello() -> str:
    """Return hello-phrase to human."""
    return {'message': 'Hello, Human!'}


@app.get('/users/', response_model=list[Users])
def get_users():
    """Return users."""
    return test_users


@app.get('/users/{user_id}/', response_model=Users)
def get_user(user_id: int):
    """Return user with given user_id."""
    return [user for user in test_users if user.get('id') == user_id][0]


@app.get('/trades/', response_model=list[Trades])
def get_trades(limit: int = 3, offset: int = 0):
    """Return trades list."""
    return test_trades[offset:][:limit]


@app.post('/trades/')
def add_trade(trades: list[Trades]):
    test_trades.extend(trades)
    return {'status': 200, "data": trades}


@app.post('/users/{user_id}/')
def change_username(user_id: int, new_username: str):
    """Change username for user with given user_id."""
    user = list(filter(lambda user: user.get('id') == user_id, test_users))[0]
    user['name'] = new_username
    return {'status': 200, 'data': user}

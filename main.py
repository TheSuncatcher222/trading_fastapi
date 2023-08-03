from fastapi import FastAPI

from models import Trade
from test_db import test_users, test_trades

app: FastAPI = FastAPI(title='Trading FastAPI App')


@app.get('/')
def say_hello() -> str:
    """Return hello-phrase to human."""
    return 'Hello, Human!'


@app.get('/users/{user_id}/')
def get_user(user_id: int) -> dict:
    """Return user with given user_id."""
    return [user for user in test_users if user.get('id') == user_id][0]


@app.get('/trades/')
def get_trades(limit: int = 3, offset: int = 0) -> list[dict]:
    """Return trades list."""
    return test_trades[offset:][:limit]


@app.post('/trades')
def add_trade(trades: list[Trade]):
    test_trades.extend(trades)
    return {'status': 200, "data": trades}


@app.post('/users/{user_id}/')
def change_username(user_id: int, new_username: str) -> dict:
    """Change username for user with given user_id."""
    user = list(filter(lambda user: user.get('id') == user_id, test_users))[0]
    user['name'] = new_username
    print(test_users)
    return {'status': 200, 'data': user}

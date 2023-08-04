from fastapi import FastAPI, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse

from app.core import SEND_DEBUG

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
def say_hello():
    """Return hello-phrase to human."""
    return {'message': 'Hello, Human!'}


# @app.get('/something/', response_model=list[Something])
# def get_example(limit: int = 3, offset: int = 0):
#     """Return something list."""
#     return Something[offset:][:limit]


# @app.get('/something/{something_id}/', response_model=Something)
# def get_id_example(user_id: int):
#     """Return something with given something_id."""
#     return [user for user in something if user.get('id') == user_id][0]


# @app.post('/users/{user_id}/')
# def post_something(something_id: int, new_something: str):
#     """Change username for user with given user_id."""
#     something = list(filter(
#         lambda something: something.get('id') == something_id, something))[0]
#     something['something'] = new_something
#     return {'status': 200, 'data': something}

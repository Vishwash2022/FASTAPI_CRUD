from fastapi import FastAPI,Request
from app import route as UsersRoute
from tortoise.contrib.fastapi import register_tortoise
from configs.connection import DATABASE_URL
from app import api as apiRoute
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware import Middleware
import typing
# from fastapi.staticfiles import StaticFiles

db_url=DATABASE_URL()
middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]
app=FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string")
# app.mount("/static",StaticFiles(directory="static"),name="static")

app.include_router(UsersRoute.router,tags=["user"])
# app.include_router(apiRoute.router,prefix="/api")





register_tortoise(
    app,
    db_url=db_url,
    modules={'models':['app.models']},
    generate_schemas  = True,
    add_exception_handlers =True
)
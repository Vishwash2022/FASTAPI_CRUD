from fastapi import FastAPI,Body
from fastapi import APIRouter, Request, Form, Depends, status
from http.client import HTTPException, HTTPResponse
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
from passlib.context import CryptContext
from fastapi.templating import Jinja2Templates
from .models import User
from starlette.templating import Jinja2Templates
import typing
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.responses import JSONResponse
import jwt
from fastapi_login import LoginManager


templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
SECRET = 'your-secret-key'
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="app/templates")
manager = LoginManager(SECRET, token_url='/auth/token')

# templates.env.globals['get_flashed_messages'] = get_flashed_messages


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def flash(request: Request, message: typing.Any, category: str = "") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
    request.session["_messages"].append(
        {"message": message, "category": category})


@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
    })


@router.post("/registration/", response_class=HTMLResponse)
async def create_user(request: Request, name: str = Form(...),
                      email: str = Form(...),
                      password: str = Form(...)):

    if "_messages" in request.session:
        print(request.session["_messages"][0]['username'])
        name = (request.session["_messages"][0]['username'])
    elif "_messages" in request.session:
        print(request.session["_messages"][0]['username'])
        email = (request.session["_messages"][0]['username'])

    else:

        user_obj = await User.create(email=email, name=name, password=get_password_hash(password))

    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/login/", response_class=HTTPResponse)
async def messg(request: Request):
    return templates.TemplateResponse("login.html", {
        "request": request,
    })


@manager.user_loader()
async def load_user(email: str):
    if await User.exists(email=email):
        newapil = await User.get(email=email)
        return newapil


@router.post('/login_user/',)
async def login(request: Request, email: str = Form(...),
                password: str = Form(...)):
    email = email
    user = await load_user(email)
    if not User:
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
    elif not verify_password(password, user.password):
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)
    else:
        # request.session['user_id']=user.id
        request.session['user_name'] = user.name
        # print(request.session["user_id"])
        print(request.session["user_name"])
        return RedirectResponse("/show_user/", status_code=status.HTTP_302_FOUND)


@router.get("/show_user/", response_class=HTTPResponse)
async def show(request: Request):
    persons = await User.all()
    return templates.TemplateResponse("show.html", {
        "persons": persons,
        "request": request
    })
    

@router.get("/del/{id}")
async def delete(request:Request,id:int):
    id=await User.get(id=id).delete()
    return RedirectResponse("/show_user/",)


# @router.post("/update_user/{id}",response_class=HTMLResponse)
# async def update(request:Request,id:int,
#                  name:str=Form(...),
#                  email:str=Form(...)):
    
#     user=await User.get(id=id).update(name=name,email=email)
#     return RedirectResponse("/show_user/", status_code=status.HTTP_302_FOUND)


@router.get("/upd/{id}",)
async def upd(request:Request,id:int):
    person=await User.get(id=id)
    return templates.TemplateResponse("upd.html", {
        "person":person,
        "request": request
    })


@router.post("/upd_user/{id}",)
async def update(request:Request,id:int,
                 name:str=Form(...),
                 email:str=Form(...)):
    await User.get(id=id).update(name=name,email=email)
    return RedirectResponse("/show_user/",)


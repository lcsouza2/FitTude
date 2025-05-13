from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


MAIN_APP = FastAPI()
MAIN_APP.mount("/static", StaticFiles(directory="web/static"), name="static")

templates = Jinja2Templates(directory="web")

@MAIN_APP.get("/")
async def return_root_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@MAIN_APP.get("/login")
async def return_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@MAIN_APP.get("/register")
async def return_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@MAIN_APP.get("/dashboard")
async def return_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
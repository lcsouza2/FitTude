from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


MAIN_APP = FastAPI()
MAIN_APP.mount("/static", StaticFiles(directory="./web/static"), name="static")

templates = Jinja2Templates(directory="./web/")

@MAIN_APP.get("/")
async def return_root_page(request: Request):
    return templates.TemplateResponse("landingpage.html", {"request": request})

@MAIN_APP.get("/login")
async def return_login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@MAIN_APP.get("/register")
async def return_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@MAIN_APP.get("/dashboard")
async def return_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@MAIN_APP.get("/active")
async def return_active_page(request: Request):
    return templates.TemplateResponse("active.html", {"request": request})

@MAIN_APP.get("/aparelhos")
async def return_aparelhos_page(request: Request):
    return templates.TemplateResponse("aparelhos.html", {"request": request})

@MAIN_APP.get("/landingpage")
async def return_landing_page(request: Request):
    return templates.TemplateResponse("landingpage.html", {"request": request})

@MAIN_APP.get("/relatorios")
async def return_relatorios_page(request: Request):
    return templates.TemplateResponse("relatorios.html", {"request": request})

@MAIN_APP.get("/configuracoes")
async def return_configuracoes_page(request: Request):
    return templates.TemplateResponse("configuracoes.html", {"request": request})

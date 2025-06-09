from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


MAIN_APP = FastAPI()
MAIN_APP.mount("/static", StaticFiles(directory="./web/static"), name="static")

templates = Jinja2Templates(directory="./web/")

@MAIN_APP.get("/")
async def return_root_page(request: Request):
    return templates.TemplateResponse("main/index.html", {"request": request})

@MAIN_APP.get("/login")
async def return_login_page(request: Request):
    return templates.TemplateResponse("main/login.html", {"request": request})

@MAIN_APP.get("/register")
async def return_register_page(request: Request):
    return templates.TemplateResponse("main/register.html", {"request": request})

@MAIN_APP.get("/dashboard")
async def return_dashboard_page(request: Request):
    return templates.TemplateResponse("main/dashboard.html", {"request": request})

@MAIN_APP.get("/active")
async def return_active_page(request: Request):
    return templates.TemplateResponse("secondary/active.html", {"request": request})

@MAIN_APP.get("/aparelhos")
async def return_aparelhos_page(request: Request):
    return templates.TemplateResponse("secondary/aparelhos.html", {"request": request})

@MAIN_APP.get("/relatorios")
async def return_relatorios_page(request: Request):
    return templates.TemplateResponse("secondary/relatorios.html", {"request": request})

@MAIN_APP.get("/exercicios")
async def return_exercicios_page(request: Request):
    return templates.TemplateResponse("secondary/exercicios.html", {"request": request})

@MAIN_APP.get("/grupamentos")
async def return_grupamentos_page(request: Request):
    return templates.TemplateResponse("secondary/grupamentos.html", {"request": request})

@MAIN_APP.get("/configuracoes")
async def return_configuracoes_page(request: Request):
    return templates.TemplateResponse("secondary/configuracoes.html", {"request": request})

@MAIN_APP.get("/check_mail")
async def return_configuracoes_page(request: Request):
    return templates.TemplateResponse("secondary/go_to_mail.html", {"request": request})

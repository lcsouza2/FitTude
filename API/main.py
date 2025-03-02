from data_get_routes import DATA_API
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from user_post_routes import USER_API

MAIN_APP = FastAPI(debug=True)

templates = Jinja2Templates(directory="./Web_App/html/")


@MAIN_APP.get("/")
async def return_index_page(http_request: Request):
    return templates.TemplateResponse(request=http_request, name="index.html")


@MAIN_APP.get("/dashboard")
async def return_dashboard_page(http_request: Request):
    return templates.TemplateResponse(request=http_request, name="dashboard.html")


MAIN_APP.mount("/static", StaticFiles(directory="./Web_App/static"))
MAIN_APP.mount("/data", DATA_API)
MAIN_APP.mount("/user", USER_API)

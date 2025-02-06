from Database.utils import validate_token
from fastapi import FastAPI, Request
import schemas
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from user_routes import POST_APP


DATA_POST_API = FastAPI(title="Requisitar criação de dados")

templates = Jinja2Templates("./Html_Templates/Web_App")

DATA_POST_API.mount(
    "/static",
    StaticFiles(directory="./Html_Templates/Web_App/static"),
    "static"
)

DATA_POST_API.mount("/main", POST_APP, "O outro post lá")

@DATA_POST_API.get("/teste")
def teste(request: Request):

    return templates.TemplateResponse(request, "test.html")


@DATA_POST_API.post("/equipment/new")
def add_custom_equipmet(http_request: Request, equipment: schemas.Equipment):
    validate_token(http_request)


@DATA_POST_API.post("/exercises/new")
def add_custom_exercise(http_request: Request): ...


@DATA_POST_API.post("/exercises/new")
def add_custom_muscle(http_request: Request): ...


@DATA_POST_API.post("/exercises/new")
def create_training_sheet(http_request: Request): ...

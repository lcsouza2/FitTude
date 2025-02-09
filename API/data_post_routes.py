from Database.utils import validate_token
from fastapi import FastAPI, Request, Depends
import schemas
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from user_routes import POST_APP
from fastapi.middleware import cors
from Database.utils import AsyncSession
from sqlalchemy import insert
import Database.db_mapping as tables


DATA_POST_API = FastAPI(title="Requisitar criação de dados")

templates = Jinja2Templates("./Html_Templates/Web_App")

DATA_POST_API.mount(
    "/static", StaticFiles(directory="./Html_Templates/Web_App/static"), "static"
)

DATA_POST_API.mount("/user", POST_APP, "O outro post lá")

DATA_POST_API.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@DATA_POST_API.get("/")
def teste(request: Request):
    return templates.TemplateResponse(request, "test.html")


@DATA_POST_API.post("/equipment/new")
async def adicionar_novo_aparelho(
    aparelho: schemas.Aparelho, user: str = Depends(validate_token)
):
    async with AsyncSession() as session:
        await session.scalars(
            insert(tables.Aparelho).values(
                {**aparelho.model_dump(), "id_usuario": int(user)}
            )
        )
        await session.commit()


@DATA_POST_API.post("/exercises/new")
def add_custom_exercise(http_request: Request): ...


@DATA_POST_API.post("/exercises/new")
def add_custom_muscle(http_request: Request): ...


@DATA_POST_API.post("/exercises/new")
def create_training_sheet(http_request: Request): ...

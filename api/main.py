from fastapi import FastAPI

from .routes.data_put_routes import DATA_PUT_API
from .routes.user_routes import USER_ROUTER

MAIN_APP = FastAPI(debug=True)

MAIN_APP.include_router(USER_ROUTER)
MAIN_APP.include_router(DATA_PUT_API)

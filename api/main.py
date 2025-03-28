from fastapi import FastAPI

from .routes.user_routes import USER_ROUTER

MAIN_APP = FastAPI(debug=True)

MAIN_APP.include_router(USER_ROUTER)
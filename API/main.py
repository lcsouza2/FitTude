from user_post_routes import USER_API
from data_post_routes import DATA_API
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


MAIN_APP = FastAPI(debug=True)

MAIN_APP.mount("/data", DATA_API)
MAIN_APP.mount("/user", USER_API)

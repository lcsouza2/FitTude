from user_routes import USER_API_POST
from data_post_routes import DATA_API_POST
from fastapi import FastAPI

MAIN_APP = FastAPI(debug=True)

@MAIN_APP.get("/def")
def abc():
    return "peido"

MAIN_APP.mount("/data", DATA_API_POST)
MAIN_APP.mount("/user", USER_API_POST)


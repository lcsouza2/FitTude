from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.security import verify_request_limit
from app.routes.data_delete_routes import DATA_DELETE_API
from app.routes.data_get_routes import DATA_GET_API
from app.routes.data_post_routes import DATA_POST_API
from app.routes.data_put_routes import DATA_PUT_API
from app.routes.user_routes import USER_ROUTER

MAIN_APP = FastAPI(debug=True)

# Apply rate limiting to all routes
MAIN_APP.include_router(USER_ROUTER, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_PUT_API, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_DELETE_API, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_GET_API, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_POST_API, dependencies=[Depends(verify_request_limit)])


MAIN_APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

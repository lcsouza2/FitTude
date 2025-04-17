from fastapi import FastAPI, Depends
from core.security import verify_request_limit
from api.routes.data_put_routes import DATA_PUT_API
from api.routes.data_delete_routes import DATA_DELETE_API  
from api.routes.data_get_routes import DATA_GET_API
from api.routes.data_post_routes import DATA_POST_API
from api.routes.user_routes import USER_ROUTER

MAIN_APP = FastAPI(debug=True, openapi_url=None, docs_url=None, redoc_url=None)

# Apply rate limiting to all routes
MAIN_APP.include_router(USER_ROUTER, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_PUT_API, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_DELETE_API, dependencies=[Depends(verify_request_limit)]) 
MAIN_APP.include_router(DATA_GET_API, dependencies=[Depends(verify_request_limit)])
MAIN_APP.include_router(DATA_POST_API, dependencies=[Depends(verify_request_limit)])

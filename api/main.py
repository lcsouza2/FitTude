from fastapi import FastAPI

app = FastAPI(debug=True)

# # Apply rate limiting to all routes
# MAIN_APP.include_router(USER_ROUTER, dependencies=[Depends(verify_request_limit)])
# MAIN_APP.include_router(DATA_PUT_API, dependencies=[Depends(verify_request_limit)])
# MAIN_APP.include_router(DATA_DELETE_API, dependencies=[Depends(verify_request_limit)])
# MAIN_APP.include_router(DATA_GET_API, dependencies=[Depends(verify_request_limit)])
# MAIN_APP.include_router(DATA_POST_API, dependencies=[Depends(verify_request_limit)])


# MAIN_APP.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:8001", "http://localhost:8001"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
#     expose_headers=["Authorization"]
# )

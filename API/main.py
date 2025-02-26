from user_routes import USER_API_POST
from data_post_routes import DATA_API_POST
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


MAIN_APP = FastAPI(debug=True)

MAIN_APP.add_middleware(
    CORSMiddleware,
    allow_origins=["http://cai-42034:8000"],  # Apenas sua origem pode acessar
    allow_credentials=True,  # Se estiver usando autenticação baseada em cookies
    allow_methods=["*"],  # Permita apenas métodos necessários
    allow_headers=["Content-Type", "Authorization"],  # Apenas os cabeçalhos necessários
)

MAIN_APP.mount("/data", DATA_API_POST)
MAIN_APP.mount("/user", USER_API_POST)


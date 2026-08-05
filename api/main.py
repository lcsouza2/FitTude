from fastapi import FastAPI
from src.routes.muscle_group_routes import router as muscle_group_router

app = FastAPI(debug=True)

app.include_router(muscle_group_router)

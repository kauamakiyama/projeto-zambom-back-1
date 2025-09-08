from fastapi import FastAPI
from app.routers import atividades, matriculas, usuarios
from app.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="API Atividades, Usuários e Matrículas - MongoDB")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(atividades.router)
app.include_router(matriculas.router)
app.include_router(usuarios.router)

@app.get("/")
def home():
    return {"message": "API de Atividades, Usuários e Matrículas - FastAPI + MongoDB"}

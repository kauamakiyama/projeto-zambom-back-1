from fastapi import APIRouter, HTTPException, status
from app.schemas import Atividade, AtividadeCreate
from bson import ObjectId
from app.database import get_database

router = APIRouter(prefix="/atividades", tags=["Atividades"])

@router.post("/", response_model=Atividade)
async def criar_atividade(atividade: AtividadeCreate):
    database = get_database()
    result = await database["atividades"].insert_one(atividade.dict())
    return {"id": str(result.inserted_id), **atividade.dict()}


@router.get("/", response_model=list[Atividade])
async def listar_atividades():
    database = get_database()
    atividades = []
    async for atividade in database["atividades"].find():
        atividades.append({
            "id": str(atividade["_id"]),
            "nome": atividade["nome"],
            "descricao": atividade["descricao"]
        })
    return atividades


@router.get("/{atividade_id}", response_model=Atividade)
async def obter_atividade(atividade_id: str):
    database = get_database()
    atividade = await database["atividades"].find_one({"_id": ObjectId(atividade_id)})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return {
        "id": str(atividade["_id"]),
        "nome": atividade["nome"],
        "descricao": atividade["descricao"]
    }


@router.delete("/{atividade_id}", response_model=dict)
async def deletar_atividade(atividade_id: str):
    database = get_database()
    result = await database["atividades"].delete_one({"_id": ObjectId(atividade_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return {"message": "Atividade removida com sucesso"}



@router.put("/{atividade_id}", response_model=Atividade)
async def atualizar_atividade(atividade_id: str, atividade: AtividadeCreate):
    database = get_database()
    result = await database["atividades"].update_one(
        {"_id": ObjectId(atividade_id)},
        {"$set": atividade.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    atividade_atualizada = await database["atividades"].find_one({"_id": ObjectId(atividade_id)})
    return {
        "id": str(atividade_atualizada["_id"]),
        "nome": atividade_atualizada["nome"],
        "descricao": atividade_atualizada["descricao"]
    }

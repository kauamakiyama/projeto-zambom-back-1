from fastapi import APIRouter, HTTPException, status
from app.schemas import Matricula, MatriculaCreate
from app.database import get_database
from bson import ObjectId

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

@router.post("/", response_model=Matricula, status_code=status.HTTP_201_CREATED)
async def criar_matricula(matricula: MatriculaCreate):
    database = get_database()

    # Verifica se o usuário existe pelo CPF
    usuario = await database["usuarios"].find_one({"cpf": matricula.cpf_usuario})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    # Verifica se a atividade existe pelo nome
    atividade = await database["atividades"].find_one({"nome": matricula.nome_atividade})
    if not atividade:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")

    result = await database["matriculas"].insert_one(matricula.dict())
    return {"id": str(result.inserted_id), **matricula.dict()}


@router.get("/", response_model=list[Matricula])
async def listar_matriculas():
    database = get_database()
    matriculas = []
    async for m in database["matriculas"].find():
        matriculas.append({
            "id": str(m["_id"]),
            "cpf_usuario": m["cpf_usuario"],
            "nome_atividade": m["nome_atividade"]
        })
    return matriculas


@router.delete("/{matricula_id}", response_model=dict)
async def deletar_matricula(matricula_id: str):
    database = get_database()
    result = await database["matriculas"].delete_one({"_id": ObjectId(matricula_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return {"message": "Matrícula removida com sucesso"}

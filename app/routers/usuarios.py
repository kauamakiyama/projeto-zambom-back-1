from fastapi import APIRouter, HTTPException, status
from app.schemas import Usuario, UsuarioCreate
from app.database import get_database
from bson import ObjectId

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=Usuario, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreate):
    database = get_database()

    # Garante que CPF seja único
    existente = await database["usuarios"].find_one({"cpf": usuario.cpf})
    if existente:
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    result = await database["usuarios"].insert_one(usuario.dict())
    return {"id": str(result.inserted_id), **usuario.dict()}


@router.get("/", response_model=list[Usuario])
async def listar_usuarios():
    database = get_database()
    usuarios = []
    async for u in database["usuarios"].find():
        usuarios.append({
            "id": str(u["_id"]),
            "nome": u["nome"],
            "idade": u["idade"],
            "email": u["email"],
            "cpf": u["cpf"],
            "endereco": u["endereco"],
            "numero": u["numero"],
            "complemento": u.get("complemento"),
            "cep": u["cep"]
        })
    return usuarios


@router.get("/{cpf}", response_model=Usuario)
async def obter_usuario(cpf: str):
    database = get_database()
    usuario = await database["usuarios"].find_one({"cpf": cpf})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {
        "id": str(usuario["_id"]),
        "nome": usuario["nome"],
        "idade": usuario["idade"],
        "email": usuario["email"],
        "cpf": usuario["cpf"],
        "endereco": usuario["endereco"],
        "numero": usuario["numero"],
        "complemento": usuario.get("complemento"),
        "cep": usuario["cep"]
    }


@router.delete("/{cpf}", response_model=dict)
async def deletar_usuario(cpf: str):
    database = get_database()
    result = await database["usuarios"].delete_one({"cpf": cpf})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return {"message": "Usuário removido com sucesso"}

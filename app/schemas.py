from pydantic import BaseModel, EmailStr
from typing import Optional

# --- Usuários ---
class UsuarioBase(BaseModel):
    nome: str
    idade: int
    email: EmailStr
    cpf: str
    endereco: str
    numero: str
    complemento: Optional[str] = None
    cep: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: str


# --- Atividades ---
class AtividadeBase(BaseModel):
    nome: str
    descricao: str

class AtividadeCreate(AtividadeBase):
    pass

class Atividade(AtividadeBase):
    id: str


# --- Matrículas ---
class MatriculaBase(BaseModel):
    cpf_usuario: str
    nome_atividade: str

class MatriculaCreate(MatriculaBase):
    pass

class Matricula(MatriculaBase):
    id: str

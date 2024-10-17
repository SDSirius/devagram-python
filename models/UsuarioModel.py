from pydantic import BaseModel, Field, EmailStr


class UsuarioModel(BaseModel):
    id:str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "email": "Digite umn e-mail valido para cadastrar um novo usuário",
            "senha": "Digite uma senha forte para cadastrar no banco de dados",
            "foto": "Selecione um arquivo de foto para caracterizar seu usuário"}

        }

class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "email": "Digite umn e-mail valido para cadastrar um novo usuário",
            "senha": "Digite uma senha forte para cadastrar no banco de dados",
            "foto": "Selecione um arquivo de foto para caracterizar seu usuário"}

        }

class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "email": "Digite umn e-mail valido para cadastrar um novo usuário",
            "senha": "Digite uma senha forte para cadastrar no banco de dados"
            }
        }

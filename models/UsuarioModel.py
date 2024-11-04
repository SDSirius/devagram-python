from pydantic import BaseModel, Field, EmailStr
from fastapi import Form, UploadFile
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()


class UsuarioModel(BaseModel):
    id:str = Field(...)
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "email": "String",
            "senha": "String",
            "foto":"String"
            }
        }


@decoratorUtil.form_body
class UsuarioCriarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "nome":"String",
            "email": "String",
            "senha": "String"
            }
        }

class UsuarioLoginModel(BaseModel):
    email: EmailStr = Field(...)
    senha: str = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "email": "String",
            "senha": "String"
            }
         }

@decoratorUtil.form_body
class UsuarioAtualizarModel(BaseModel):
    nome: str = Field(...)
    email: EmailStr = Field(...)
    senha: str = Field(...)
    foto: UploadFile = Field(...)

    class Config:
        json_schema_extra = {
            "usuario": {
            "nome":"String",
            "email": "String",
            "senha": "String"
            }
        }

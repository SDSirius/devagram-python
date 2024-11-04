from fastapi import UploadFile
from pydantic import BaseModel, Field
from typing import List
from models.ComentarioModel import ComentarioModel
from models.UsuarioModel import UsuarioModel
from utils.DecoratorUtil import DecoratorUtil

decoratorUtil = DecoratorUtil()
class PostagemModel(BaseModel):
    id: str = Field(...)
    usuario_id: str = Field(...)
    foto: str = Field(...)
    legenda: str = Field(...)
    data: str
    curtidas: List
    comentarios: List

    class Config:
        json_schema_extra = {
            "Postagem": {
                "id": "string",
                "usuario_id": "UsuarioModel",
                "foto": "string",
                "legenda": "string",
                "data": "string",
                "curtidas": "List[usuario_id]",
                "comentarios": "List[comentarios]"

            }
        }
@decoratorUtil.form_body
class PostagemCriarModel(BaseModel):
    foto: UploadFile = Field(...)
    legenda: str = Field(...)

    class Config:
        json_schema_extra = {
            "Postagem": {
                "foto": "string",
                "legenda": "string"

            }
        }
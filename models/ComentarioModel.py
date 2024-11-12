from pydantic import BaseModel, Field


class ComentarioModel(BaseModel):
    comentario_id: str = Field(...)
    usuario_id: str = Field(...)
    comentario: str = Field(...)

    class Config:
        json_schema_extra = {
            "Comentario": {
                "comentario_id": "String",
                "usuario_id": "string",
                "comentario": "String"
            }
        }

class ComentarioCriarModel(BaseModel):
    comentario: str = Field(...)

    class Config:
        json_schema_extra = {
            "Comentario": {
                "comentario": "string"
            }
        }

class ComentarioAtualizarModel(BaseModel):
    comentario: str = Field(...)
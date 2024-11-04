from pydantic import BaseModel, Field


class ComentarioModel(BaseModel):
    usuario_id: str = Field(...)
    comentario: str = Field(...)
    data: str

    class Config:
        json_schema_extra = {
            "Comentario": {
                "usuario": "String",
                "comentario": "string",
                "data": "String"
            }
        }

class ComentarioCriarModel(BaseModel):
    comentario: str = Field(...)

    # class Config:
    #     json_schema_extra = {
    #         "Comentario": {
    #             "comentario": "string"
    #         }
    #     }
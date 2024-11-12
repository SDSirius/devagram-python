from models.PostagemModel import PostagemModel
from models.UsuarioModel import UsuarioModel

class ConverterUtil:
    def usuario_converter(self, usuario):
        return UsuarioModel(
            id=str(usuario.get("_id", "")),
            nome=usuario.get("nome", ""),
            email=usuario.get("email", ""),
            senha=usuario.get("senha", ""),
            foto=usuario.get("foto", ""),
            seguidores=[str(p) for p in usuario.get("seguidores", [])],
            seguindo=[str(p) for p in usuario.get("seguindo", [])],
            total_seguidores=usuario.get("total_seguidores", 0),
            total_seguindo=usuario.get("total_seguindo", 0),
            postagens=usuario.get("postagens", []),
            total_postagens=usuario.get("total_postagens", 0),
            token=usuario.get("token", "")
        )

    def postagem_converter(self, postagem):
        return PostagemModel(
            id=str(postagem["_id"]) if "_id" in postagem else "",
            usuario_id=str(postagem["usuario_id"]) if "usuario_id" in postagem else "",
            foto=postagem["foto"] if "foto" in postagem else "",
            legenda=postagem["legenda"] if "legenda" in postagem else "",
            data=str(postagem["data"]) if "data" in postagem else "",
            curtidas=[str(p) for p in postagem["curtidas"]] if "curtidas" in postagem else [],
            comentarios=[
                {
                    "comentario": p["comentario"],
                    "comentario_id": str(p["comentario_id"]),
                    "usuario_id": str(p["usuario_id"])
                } for p in postagem["comentarios"]
            ] if "comentarios" in postagem else "",
            usuario=self.usuario_converter(postagem["usuario"][0]) if "usuario" in postagem and len(postagem["usuario"])>0 else None,
            total_curtidas=postagem["total_curtidas"] if "total_curtidas" in postagem else 0,
            total_comentarios=postagem["total_comentarios"] if "total_comentarios" in postagem else 0,
        )
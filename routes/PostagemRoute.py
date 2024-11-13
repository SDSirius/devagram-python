from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body

from middlewares.JWTMiddleware import verificar_token
from models.ComentarioModel import ComentarioModel, ComentarioCriarModel, ComentarioAtualizarModel
from models.PostagemModel import PostagemCriarModel
from services.UsuarioService import UsuarioService
from services.AuthService import AuthService
from services.PostagemService import PostagemService

router = APIRouter()
authService = AuthService()
usuarioService = UsuarioService()
postagemService = PostagemService()

@router.post(
    "/",
    response_description="Rota para criar uma nova postagem",
    dependencies=[Depends(verificar_token)]
)
async def criar_postagem(Authorization:str = Header(default=''), postagem: PostagemCriarModel= Depends(PostagemCriarModel)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado.id)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro

@router.get(
    '/',
    response_description="Rota para listar as postagens.",
    dependencies=[Depends(verificar_token)])
async def listar_postagens():
    try:
        resultado = await postagemService.listar_postagens()

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

@router.get(
    '/{usuario_id}',
    response_description="Rota para listar as postagens de um usuario.",
    dependencies=[Depends(verificar_token)])
async def listar_postagens_usuario(usuario_id: str, Authorization:str = Header(default='')):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)
        resultado = await postagemService.listar_postagens_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro


@router.put(
    '/curtir/{postagem_id}',
    response_description="Rota para curtir ou descurtir uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir_postagem(postagem_id: str, Authorization: str = Header(default='')):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)
        resultado = await postagemService.curtir_descurtir(postagem_id, usuario_logado.id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

@router.put(
    '/comentar/{postagem_id}',
    response_description="Rota para ccomentar em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def comentar_postagem(postagem_id: str, comentario_model: ComentarioCriarModel = Body(...), Authorization: str = Header(default='') ):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await postagemService.criar_comentario(postagem_id,usuario_logado.id , comentario_model.comentario)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

@router.delete(
    '/{postagem_id}',
    response_description="Rota para deletar uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_postagem(postagem_id: str, Authorization: str = Header(default='') ):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await postagemService.deletar_postagem(postagem_id, usuario_logado.id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

@router.delete(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para deletar comentario em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def deletar_comentario(postagem_id: str, comentario_id:str, Authorization: str = Header(default='') ):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await postagemService.deletar_comentario(postagem_id,usuario_logado.id, comentario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

@router.put(
    '/{postagem_id}/comentario/{comentario_id}',
    response_description="Rota para atualizar um  comentario.",
    dependencies=[Depends(verificar_token)]
)
async def atualizar_comentario(postagem_id: str, comentario_id:str, Authorization: str = Header(default=''), comentario_model: ComentarioAtualizarModel = Body(...) ):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await postagemService.atualizar_comentario(postagem_id,usuario_logado.id, comentario_id, comentario_model.comentario)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as erro:
        print(erro)
        raise erro

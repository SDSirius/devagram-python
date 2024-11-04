from fastapi import APIRouter, HTTPException, Depends, Header, UploadFile, Body

from middlewares.JWTMiddleware import verificar_token
from models.ComentarioModel import ComentarioModel, ComentarioCriarModel
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
async def rota_criar_postagem(Authorization:str = Header(default=''), postagem: PostagemCriarModel= Depends(PostagemCriarModel)):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decodificar_token_jwt(token)
        resultado_usuario = await usuarioService.buscar_usuario_logado(payload['usuario_id'])
        usuario_logado = resultado_usuario['dados']


        resultado = await postagemService.cadastrar_postagem(postagem, usuario_logado['_id'])

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:
        raise error

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

    except Exception as error:
        print(error)
        raise error

# @router.get(
#     '/me',
#     response_description="Rota para listar as postagens do usuario logado.",
#     dependencies=[Depends(verificar_token)])
# async def listar_postagens_usuario_logado(Authorization:str = Header(default='')):
#     try:
#
#         return {"resultado":"teste usuario logado"}
#
#     except Exception as error:
#         print(error)
#         raise error


@router.put(
    '/curtir/{postagem_id}',
    response_description="Rota para curtir ou descurtir uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def curtir_descurtir_postagem(postagem_id: str, Authorization: str = Header(default='')):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decodificar_token_jwt(token)
        resultado_usuario = await usuarioService.buscar_usuario_logado(payload['usuario_id'])
        usuario_logado = resultado_usuario['dados']

        resultado = await postagemService.curtir_descurtir(postagem_id, usuario_logado['_id'])

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as error:
        print(error)
        raise error

@router.put(
    '/comentar/{postagem_id}',
    response_description="Rota para ccomentar em uma postagem",
    dependencies=[Depends(verificar_token)]
)
async def comentar_postagem(postagem_id: str, comentario_model: ComentarioCriarModel = Body(...), Authorization: str = Header(default='') ):
    try:
        token = Authorization.split(' ')[1]
        payload = authService.decodificar_token_jwt(token)
        resultado_usuario = await usuarioService.buscar_usuario_logado(payload['usuario_id'])
        usuario_logado = resultado_usuario['dados']

        resultado = await postagemService.criar_comentario(postagem_id, usuario_logado["_id"], comentario_model.comentario)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as error:
        print(error)
        raise error
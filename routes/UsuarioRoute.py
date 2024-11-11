import os
from datetime import datetime
from fastapi import APIRouter, Body, HTTPException, Depends, Header, UploadFile
from middlewares.JWTMiddleware import verificar_token
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from services.AuthService import AuthService
from services.UsuarioService import UsuarioService

router = APIRouter()
usuarioService = UsuarioService()
authService = AuthService()

@router.post(
    "/",
    response_description="Rota para criar um novo Usuário"
)
async def rota_criar_usuario(file : UploadFile, usuario: UsuarioCriarModel= Depends(UsuarioCriarModel)):
    try:
        caminho_foto = f'files/foto-{datetime.now().strftime('%H%M%S')}.png'

        with open(caminho_foto, 'wb+') as arquivo:
            arquivo.write(file.file.read())

        resultado = await usuarioService.registrar_usuario(usuario, caminho_foto)

        os.remove(caminho_foto)

        if not resultado.status == 201:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as error:

        raise error

@router.get(
    '/me',
    response_description="Rota para buscar as informações do usuário logado",
    dependencies=[Depends(verificar_token)])
async def buscar_info_usuario_logado(Authorization:str = Header(default='')):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)
        print(usuario_logado)
        resultado = await usuarioService.buscar_usuario(usuario_logado.id)


        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        del resultado.dados.senha

        return resultado

    except Exception as error:
        print(error)
        raise error

@router.get(
    '/{usuario_id}',
    response_description="Rota para buscar as informações do usuário logado",
    dependencies=[Depends(verificar_token)])
async def buscar_info_usuario(usuario_id: str):
    try:
        resultado = await usuarioService.buscar_usuario(usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        del resultado.dados.senha

        return resultado

    except Exception as error:
        print(error)
        raise error

@router.get(
    '/',
    response_description="Rota para listar todos usuários.",
    dependencies=[Depends(verificar_token)])
async def listar_usuarios(nome: str):
    try:
        resultado = await usuarioService.listar_usuarios(nome)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)
        return resultado

    except Exception as error:
        print(error)
        raise error

@router.put(
    '/me',
    response_description='Rota para atualizar as informações do usuário logado.',
    dependencies=[Depends(verificar_token)]
    )
async def atualizar_usuario_logado(Authorization: str = Header(default=''), usuario_atualizar: UsuarioAtualizarModel = Depends(UsuarioAtualizarModel)):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)

        resultado = await usuarioService.atualizar_usuario_logado(usuario_logado.id, usuario_atualizar)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado
    except Exception as erro:
        raise erro

@router.put(
    '/seguir/{usuario_id}',
    response_description="Rota para seguir/Deixar de seguir um usuario.",
    dependencies=[Depends(verificar_token)]
)
async def seguir_desseguir(usuario_id: str, Authorization: str = Header(default='') ):
    try:
        usuario_logado = await authService.buscar_usuario_logado(Authorization)
        print(usuario_logado.id)
        print(usuario_id)

        if usuario_id == usuario_logado["id"]:
            raise HTTPException(status_code=401, detail="você não pode seguir a si mesmo!")

        resultado = await usuarioService.seguir_desseguir(usuario_logado["id"], usuario_id)

        if not resultado.status == 200:
            raise HTTPException(status_code=resultado.status, detail=resultado.mensagem)

        return resultado

    except Exception as error:
        print(error)
        raise error
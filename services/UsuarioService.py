from datetime import datetime
import os
from dtos.ResponseDTO import ResponseDTO
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.UsuarioRepository import UsuarioRepository

awsProvider = AWSProvider()
usuarioRepository = UsuarioRepository()

class UsuarioService:

    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

            if usuario_encontrado:
                return {
                    "mensagem": f'Email {usuario.email} já cadastrado no sistema',
                    "dados": "",
                    "status":400
                }
            else:
                novo_usuario = await usuarioRepository.criar_usuario(usuario)

                try:
                    url_foto = awsProvider.upload_arquivo_s3(
                        f'fotos-perfil/{novo_usuario["_id"]}.png',
                        caminho_foto
                    )

                    novo_usuario = await usuarioRepository.atualizar_usuario(novo_usuario["_id"], {"foto": url_foto})

                except Exception as erroAws:
                    print("erroAws " + str(erroAws))

                return {
                    "mensagem": "Usuario criado com sucesso",
                    "dados": novo_usuario,
                    "status": 201
                }

        except Exception as error:
            return {
                "mensagem": "Erro Interno no servidor",
                "dados": str(error),
                "status": 500
            }

    async def buscar_usuario_logado(self, id:str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario(id)

            if usuario_encontrado:
                return {
                    "mensagem": f'Usuário encontrado',
                    "dados": usuario_encontrado,
                    "status": 200
                }

            else:
                return {
                    "mensagem": f'Usuário com o id {id} não encontrado',
                    "dados":"" ,
                    "status": 404
                }

        except Exception as error:
            return {
                "mensagem": "Erro Interno no servidor",
                "dados": str(error),
                "status": 500
            }

    async def atualizar_usuario_logado(self, id, usuario_atualizar: UsuarioAtualizarModel):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario(id)

            if usuario_encontrado:
                usuario_dict = usuario_atualizar.__dict__

                try:
                    caminho_foto = f'files/foto-{datetime.now().strftime("%H%M%S")}.png'

                    with open(caminho_foto, 'wb+') as arquivo:
                        arquivo.write(usuario_atualizar.foto.file.read())

                    url_foto = awsProvider.upload_arquivo_s3(
                        f'fotos-perfil/{id}.png',
                        caminho_foto
                    )

                    os.remove(caminho_foto)
                except Exception as erro:
                    print(erro)

                usuario_dict['foto'] = url_foto if url_foto is not None else usuario_dict['foto']

                usuario_atualizado = await usuarioRepository.atualizar_usuario(id, usuario_dict)

                return ResponseDTO("Usuário atualizado.", usuario_atualizado, 200)
            else:
                return ResponseDTO(f"Usuário com o id {id} não foi encontrado.", "", 404)

        except Exception as erro:
            print(erro)

            return ResponseDTO("Erro interno no servidor", str(erro), 500)
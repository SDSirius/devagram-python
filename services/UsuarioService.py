from datetime import datetime
import os
from bson import ObjectId
from dtos.ResponseDTO import ResponseDTO
from models.UsuarioModel import UsuarioCriarModel, UsuarioAtualizarModel
from providers.AWSProvider import AWSProvider
from repositories.PostagemRepository import PostagemRepository
from repositories.UsuarioRepository import UsuarioRepository

awsProvider = AWSProvider()
usuarioRepository = UsuarioRepository()
postagemRepository = PostagemRepository()

class UsuarioService:

    async def registrar_usuario(self, usuario: UsuarioCriarModel, caminho_foto):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario_por_email(usuario.email)

            if usuario_encontrado:
                return ResponseDTO(f'Email {usuario.email} já cadastrado no sistema', "", 400)

            else:
                novo_usuario = await usuarioRepository.criar_usuario(usuario)
                try:
                    url_foto = awsProvider.upload_arquivo_s3(
                        f'fotos-perfil/{novo_usuario.id}.png',
                        caminho_foto
                    )

                    novo_usuario = await usuarioRepository.atualizar_usuario(novo_usuario.id, {"foto": url_foto})

                except Exception as erroAws:
                    print("erroAws " + str(erroAws))

                return ResponseDTO("Usuario criado com sucesso",novo_usuario, 201)

        except Exception as erro:
            return ResponseDTO("Erro Interno no servidor", str(erro), 500)

    async def buscar_usuario(self, id: str):
        try:
            usuario_encontrado = await usuarioRepository.buscar_usuario(id)

            if usuario_encontrado:
                postagens_encontradas = await postagemRepository.listar_postagens_usuario(id)

                usuario_encontrado.total_seguidores = len(usuario_encontrado.seguidores)
                usuario_encontrado.total_seguindo = len(usuario_encontrado.seguindo)
                usuario_encontrado.postagens = postagens_encontradas
                usuario_encontrado.total_postagens = len(postagens_encontradas)

                return ResponseDTO("Usuário encontrado.", usuario_encontrado, 200)
            else:
                return ResponseDTO(f"Usuário com o id {id} não foi encontrado.", "", 404)

        except Exception as erro:
            print(erro)

            return ResponseDTO("Erro interno no servidor", str(erro), 500)

    async def listar_usuarios(self, nome):
        try:
            usuarios_encontrados = await usuarioRepository.listar_usuarios(nome)
            for u in usuarios_encontrados:
                del u.senha
                u.total_seguindo = len(u.seguindo)
                u.total_seguidores = len(u.seguidores)

            return ResponseDTO("Usuarios listados", usuarios_encontrados, 200)


        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)

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

    async def seguir_desseguir(self, usuario_logado_id, usuario_seguido_id):
        try:

            if usuario_logado_id == usuario_seguido_id:
                return ResponseDTO("Você não pode seguir a sí mesmo!", "", 500)

            usuario_logado_encontrado = await usuarioRepository.buscar_usuario(usuario_logado_id)
            usuario_seguido_encontrado = await usuarioRepository.buscar_usuario(usuario_seguido_id)



            if usuario_seguido_encontrado.seguidores.count(usuario_logado_id) > 0:
                usuario_seguido_encontrado.seguidores.remove(usuario_logado_id)
                usuario_logado_encontrado.seguindo.remove(usuario_seguido_id)

            else:
                usuario_seguido_encontrado.seguidores.append(ObjectId(usuario_logado_id))
                usuario_logado_encontrado.seguindo.append(ObjectId(usuario_seguido_id))

            await usuarioRepository.atualizar_usuario(
                usuario_seguido_encontrado.id,{
                    "seguidores": usuario_seguido_encontrado.seguidores
                }
            )
            await usuarioRepository.atualizar_usuario(
                usuario_logado_encontrado.id, {
                    'seguindo': usuario_logado_encontrado.seguindo
                }
            )

            return ResponseDTO("Usuario Seguido com sucesso!", "", 200)

        except Exception as erro:
            print(erro)
            return ResponseDTO("Erro interno no servidor", str(erro), 500)
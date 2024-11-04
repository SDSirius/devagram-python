from fastapi import FastAPI
from routes.UsuarioRoute import router as UsuarioRoute
from routes.PostagemRoute import router as PostagemRoute
from routes.AutenticacaoRoute import router as AutenticacaoRoute


app = FastAPI()

app.include_router(UsuarioRoute, tags=["Usuário"], prefix="/api/usuario")
app.include_router(AutenticacaoRoute, tags=["Autenticação"], prefix="/api/auth")
app.include_router(PostagemRoute, tags=["Postagem"], prefix="/api/postagem")


@app.get("/api/health", tags=["Health"])
async def health():
    return {
        "status": "OK!"
    }
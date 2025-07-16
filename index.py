# index.py - Versão final para Railway (API-only)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import verificar

app = FastAPI()

# Configuração de CORS para permitir que a Netlify acesse a API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui o endpoint /api/verificar
app.include_router(verificar.router)

# Rota de status para verificar se a API está online
@app.get("/")
def status_check():
    return {"status": "API online"}
    
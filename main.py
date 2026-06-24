"""
Entry point para o microsserviço Robô de Atendimento IA.
Roda de forma independente, conteinerizado, sem dependência do backend principal.
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from router import router

app = FastAPI(
    title="Robô de Atendimento IA",
    description="Microsserviço de chatbot para atendimento ao cliente via LangChain + OpenAI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000")
allowed_origins = [o.strip() for o in _origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-User-Id"],
)


@app.get("/")
async def root():
    return {"service": "robo_ia_atendimento", "status": "running"}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "robo_ia_atendimento"}


app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8002))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

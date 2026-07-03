"""
Router do Robô de Atendimento IA.
Microsserviço independente — não depende do backend principal.
"""
import os
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/robo", tags=["Customer Service Robot AI"])


class ChatRequest(BaseModel):
    session_id: str
    message: str
    restaurant_name: Optional[str] = "nosso restaurante"
    restaurant_id: Optional[str] = None
    slug: Optional[str] = None
    source: Optional[str] = "website"


class ChatResponse(BaseModel):
    session_id: str
    response: str
    intent: str


SOURCE_PROMPTS = {
    "whatsapp": "Você está atendendo um cliente via WhatsApp. Seja direto e use emojis com moderação.",
    "facebook": "Você está atendendo um cliente via Facebook Messenger. Mantenho tom profissional e amigável.",
    "instagram": "Você está atendendo um cliente via Instagram Direct. Use linguagem jovem e descontraída.",
    "telegram": "Você está atendendo um cliente via Telegram. Seja objetivo e claro.",
    "website": "Você está atendendo um cliente via chat do site. Seja prestativo e educado.",
}


@router.post("/chat", response_model=ChatResponse)
async def chat_with_robot(payload: ChatRequest) -> ChatResponse:
    """Interagir com o robô de atendimento via IA."""
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="A mensagem não pode ser vazia.")

    source = payload.source or "website"
    channel_hint = SOURCE_PROMPTS.get(source, SOURCE_PROMPTS["website"])

    deepseek_api_key = os.environ.get("DEEPSEEK_API_KEY", "")

    if not deepseek_api_key or "sua-chave-deepseek" in deepseek_api_key:
        return ChatResponse(
            session_id=payload.session_id,
            response=(
                f"Olá! Sou o assistente virtual de {payload.restaurant_name}. "
                f"No momento estou em modo de simulação. Você disse: '{payload.message}'. "
                "Como posso ajudar?"
            ),
            intent="mock_fallback",
        )

    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage, SystemMessage

        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=deepseek_api_key,
            base_url="https://api.deepseek.com/v1",
        )

        system_prompt = (
            f"Você é um assistente virtual de atendimento para {payload.restaurant_name}. "
            f"{channel_hint} "
            "Ajude clientes com pedidos, cardápio, preços, horários de funcionamento, "
            "formas de pagamento e delivery. "
            "Se não souber responder algo, peça desculpas e sugira falar com um atendente humano. "
            "Mantenha respostas curtas (máximo 3 parágrafos). "
            "Sempre trate o cliente com cordialidade e paciência."
        )

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=payload.message),
        ]

        ai_response = llm.invoke(messages)
        return ChatResponse(
            session_id=payload.session_id,
            response=ai_response.content,
            intent="general_query",
        )

    except Exception as exc:
        print(f"[robo_ia_atendimento] Erro ao chamar Deepseek: {exc}")
        return ChatResponse(
            session_id=payload.session_id,
            response="Desculpe, ocorreu um erro técnico. Nossa equipe já foi notificada.",
            intent="error",
        )

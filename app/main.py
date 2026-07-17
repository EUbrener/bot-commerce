import logging
from contextlib import asynccontextmanager
from typing import Optional, List, Tuple, Dict, Any
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.nlp.classifier import load_classifier
from app.nlp.faq import load_faq_models
from app.services.chatbot_service import processar_mensagem, obter_analytics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events for FastAPI to load resources on startup."""
    logger.info("Iniciando o servidor FastAPI e carregando modelos...")
    try:
        # Load classification models
        load_classifier()
        # Load FAQ models
        load_faq_models()
        logger.info("Todos os modelos foram carregados com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao carregar modelos no startup: {e}")
        logger.warning("O servidor iniciou sem os arquivos de modelo. Certifique-se de executar 'python train.py'.")
    yield
    logger.info("Encerrando o servidor...")

app = FastAPI(
    title="🤖 Chatbot E-commerce API",
    description="API de atendimento automático para e-commerce usando Processamento de Linguagem Natural.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust for production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount static files to serve frontend assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/", response_class=FileResponse, summary="Retorna a página de e-commerce com o chatbot de suporte")
async def get_index():
    return FileResponse("app/static/index.html")

# Pydantic Schemas for validation
class ChatMessageInput(BaseModel):
    mensagem: str = Field(..., description="A mensagem enviada pelo usuário", example="Como posso rastrear meu pedido?")
    historico: Optional[List[Tuple[str, str]]] = Field(None, description="Histórico de conversas anteriores (lista de tuplas usuário-bot)")

class SentimentResult(BaseModel):
    sentimento: str = Field(..., example="neutro")
    confianca: float = Field(..., example=0.76)
    estrelas: int = Field(..., example=3)

class EntityDetail(BaseModel):
    valores: List[str] = Field(default_factory=list)
    validos: List[str] = Field(default_factory=list)

class EntitiesResult(BaseModel):
    pedidos: EntityDetail
    datas: EntityDetail
    valores: EntityDetail
    emails: EntityDetail
    telefones: EntityDetail

class ChatResponse(BaseModel):
    resposta: str = Field(..., description="A resposta formatada enviada pelo bot")
    intencao: str = Field(..., description="Intenção classificada pelo modelo")
    confianca: float = Field(..., description="Confiança na classificação da intenção")
    entidades: EntitiesResult = Field(..., description="Entidades extraídas e validadas")
    requer_humano: bool = Field(..., description="Indica se a chamada precisa de operador humano")
    nivel_busca: Optional[str] = Field(None, description="Indica o nível do FAQ acionado (tfidf, bigrama, sugestoes)")
    sentimento: SentimentResult = Field(..., description="Resultado da análise de sentimento")

class AnalyticsResult(BaseModel):
    total_mensagens: int
    escalacoes_humano: int
    confianca_media: float
    intencoes: Dict[str, int]
    sentimentos: Dict[str, int]
    faq_matches: Dict[str, int]
    entidades_extraidas: Dict[str, int]

@app.post("/chat", response_model=ChatResponse, summary="Envia uma mensagem ao chatbot")
async def chat_endpoint(payload: ChatMessageInput):
    """
    Processa a mensagem enviada pelo usuário utilizando o pipeline central de NLP.
    Retorna o roteamento, intenções, entidades extraídas, sentimento e a resposta gerada.
    """
    try:
        resultado = processar_mensagem(payload.mensagem, payload.historico)
        return resultado
    except FileNotFoundError as fnf:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Serviço temporariamente indisponível: modelos não carregados. {str(fnf)}"
        )
    except Exception as e:
        logger.error(f"Erro ao processar mensagem no endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro interno ao processar a mensagem: {str(e)}"
        )

@app.get("/analytics", response_model=AnalyticsResult, summary="Retorna métricas de analytics do chatbot")
async def analytics_endpoint():
    """
    Retorna estatísticas detalhadas sobre o uso do chatbot,
    incluindo intenções frequentes, sentimentos, acionamento do FAQ e entidades.
    """
    return obter_analytics()

@app.get("/health", summary="Verifica a integridade da API e se os modelos estão carregados")
async def health_endpoint():
    """
    Endpoint simples para monitorar se a API está online e se os arquivos de ML foram
    corretamente treinados e carregados.
    """
    try:
        # Tenta verificar se os modelos estão na memória
        load_classifier()
        load_faq_models()
        return {"status": "healthy", "models_loaded": True}
    except Exception:
        return {"status": "unhealthy", "models_loaded": False, "message": "Modelos ausentes. Execute 'python train.py'"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

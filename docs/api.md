# Contratos de API

A aplicação expõe uma API RESTful utilizando FastAPI, com documentação automática baseada no padrão OpenAPI.

## Endpoints Principais

### `GET /`
Retorna a página inicial (frontend) estática do e-commerce com o chatbot de suporte incorporado.

### `POST /chat`
Endpoint principal para interação com o chatbot. Recebe a requisição, orquestra o pipeline central de NLP para classificar a intenção, processar entidades e calcular sentimentos.

**Request Body (JSON):**
```json
{
  "mensagem": "Como posso rastrear meu pedido 12345?",
  "historico": [
    ["Oi", "Olá! Como posso te ajudar?"]
  ]
}
```

**Response (JSON):**
```json
{
  "resposta": "Para rastrear seu pedido, acesse a aba 'Meus Pedidos'.",
  "intencao": "rastrear_pedido",
  "confianca": 0.89,
  "entidades": {
    "pedidos": {"valores": ["12345"], "validos": ["12345"]},
    "datas": {"valores": [], "validos": []},
    "valores": {"valores": [], "validos": []},
    "emails": {"valores": [], "validos": []},
    "telefones": {"valores": [], "validos": []}
  },
  "requer_humano": false,
  "nivel_busca": null,
  "sentimento": {
    "sentimento": "neutro",
    "confianca": 0.95,
    "estrelas": 3
  }
}
```

### `GET /analytics`
Retorna métricas e estatísticas detalhadas sobre o uso e eficácia do chatbot, incluindo histórico de intenções capturadas, nível de confiança média e quantidade de acionamentos de atendimento humano.

### `GET /health`
Endpoint para monitorar integridade da aplicação e certificar que todos os modelos ML requeridos pelo sistema foram corretamente treinados e carregados na memória.

> [!TIP]
> Com a API FastAPI rodando (via Uvicorn), você pode acessar a especificação interativa completa do OpenAPI (Swagger UI) navegando até `/docs` no host do servidor local (ex: `http://localhost:8000/docs`).

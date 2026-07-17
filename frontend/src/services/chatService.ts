// Serviço centralizado de chat integrado com o backend FastAPI do bot.
// Endpoint: POST http://localhost:8000/chat
// Payload: { mensagem: string, historico: [ [user, bot], ... ] }

export type ChatHistorico = Array<[string, string]>;

export interface ChatRequest {
  mensagem: string;
  historico: ChatHistorico;
}

export interface ChatResponse {
  resposta: string;
  requer_humano?: boolean;
  numero_pedido?: string;
  [k: string]: unknown;
}

const API_URL =
  (typeof import.meta !== "undefined" &&
    (import.meta as unknown as { env?: Record<string, string> }).env
      ?.VITE_CHAT_API_URL) ||
  "http://localhost:8000/chat";

export async function enviarMensagem(
  mensagem: string,
  historico: ChatHistorico,
): Promise<ChatResponse> {
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ mensagem, historico } satisfies ChatRequest),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = (await res.json()) as ChatResponse;
    return data;
  } catch (err) {
    // Fallback local para permitir uso sem backend rodando.
    return mockResposta(mensagem);
  }
}

function mockResposta(msg: string): ChatResponse {
  const m = msg.toLowerCase();
  if (m.includes("humano") || m.includes("atendente") || m.includes("reclamação")) {
    return {
      resposta:
        "Entendi. Vou te encaminhar para um de nossos atendentes humanos agora mesmo.",
      requer_humano: true,
    };
  }
  if (m.includes("rastre") || m.includes("pedido")) {
    return {
      resposta:
        "Seu pedido PED-123456 está a caminho! Previsão de entrega: 3 dias úteis.",
      numero_pedido: "PED-123456",
    };
  }
  if (m.includes("pagamento") || m.includes("pagar")) {
    return {
      resposta:
        "Aceitamos Pix, boleto e cartão de crédito em até 12x sem juros. 💳",
    };
  }
  if (m.includes("reembolso") || m.includes("devolu")) {
    return {
      resposta:
        "Você tem até 7 dias após o recebimento para solicitar reembolso. O valor retorna em até 5 dias úteis.",
    };
  }
  return {
    resposta:
      "Olá! Sou o assistente virtual da GadgetBR. Posso ajudar com pedidos, pagamentos, entrega e trocas. O que você precisa?",
  };
}

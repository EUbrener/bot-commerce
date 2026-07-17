import { useEffect, useRef, useState } from "react";
import { MessageSquare, X, Send, Bot, User, AlertCircle } from "lucide-react";
import { enviarMensagem, type ChatHistorico } from "@/services/chatService";

interface Mensagem {
  autor: "user" | "bot";
  texto: string;
}

const SUGESTOES = [
  "Como rastrear meu pedido?",
  "Quais formas de pagamento?",
  "Como funciona o reembolso?",
];

export function Chatbot() {
  const [aberto, setAberto] = useState(false);
  const [mensagens, setMensagens] = useState<Mensagem[]>([
    {
      autor: "bot",
      texto:
        "Olá! 👋 Sou o assistente virtual da GadgetBR. Como posso ajudar você hoje?",
    },
  ]);
  const [input, setInput] = useState("");
  const [carregando, setCarregando] = useState(false);
  const [requerHumano, setRequerHumano] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({
      top: scrollRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [mensagens, carregando]);

  const historico = (): ChatHistorico => {
    const h: ChatHistorico = [];
    for (let i = 0; i < mensagens.length; i++) {
      if (mensagens[i].autor === "user") {
        const prox = mensagens[i + 1];
        if (prox && prox.autor === "bot") {
          h.push([mensagens[i].texto, prox.texto]);
          i++;
        }
      }
    }
    return h;
  };

  async function enviar(texto: string) {
    const t = texto.trim();
    if (!t || carregando) return;
    setInput("");
    setMensagens((m) => [...m, { autor: "user", texto: t }]);
    setCarregando(true);
    const resp = await enviarMensagem(t, historico());
    setCarregando(false);
    if (resp.requer_humano) setRequerHumano(true);
    setMensagens((m) => [...m, { autor: "bot", texto: resp.resposta }]);
  }

  return (
    <>
      {/* Floating button */}
      {!aberto && (
        <button
          onClick={() => setAberto(true)}
          aria-label="Abrir chat"
          className="fixed bottom-6 right-6 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 transition-transform hover:scale-105"
        >
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-indigo-500 opacity-40" />
          <MessageSquare className="relative h-6 w-6" />
        </button>
      )}

      {/* Chat window */}
      {aberto && (
        <div className="fixed bottom-6 right-6 z-50 flex h-[540px] w-[92vw] max-w-sm animate-scale-in flex-col overflow-hidden rounded-2xl border border-border bg-white shadow-2xl">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-border bg-gradient-to-br from-indigo-600 to-indigo-700 px-4 py-3 text-white">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-full bg-white/15">
                <Bot className="h-5 w-5" />
              </div>
              <div>
                <p className="text-sm font-semibold leading-tight">
                  Assistente Virtual
                </p>
                <p className="flex items-center gap-1.5 text-[11px] opacity-90">
                  <span
                    className={`inline-block h-2 w-2 rounded-full ${
                      requerHumano
                        ? "bg-orange-400 animate-pulse"
                        : "bg-green-400 animate-pulse"
                    }`}
                  />
                  {requerHumano ? "Encaminhando..." : "Online"}
                </p>
              </div>
            </div>
            <button
              onClick={() => setAberto(false)}
              aria-label="Fechar chat"
              className="rounded-md p-1 opacity-80 hover:bg-white/10 hover:opacity-100"
            >
              <X className="h-5 w-5" />
            </button>
          </div>

          {/* Alerta atendimento humano */}
          {requerHumano && (
            <div className="flex items-start gap-2 border-b border-orange-200 bg-orange-50 px-4 py-2 text-xs text-orange-800">
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>Encaminhando para um atendente humano...</span>
            </div>
          )}

          {/* Mensagens */}
          <div
            ref={scrollRef}
            className="flex-1 space-y-3 overflow-y-auto bg-slate-50 px-4 py-4"
          >
            {mensagens.map((m, i) => (
              <div
                key={i}
                className={`flex items-end gap-2 ${
                  m.autor === "user" ? "justify-end" : "justify-start"
                }`}
              >
                {m.autor === "bot" && (
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                    <Bot className="h-4 w-4" />
                  </div>
                )}
                <div
                  className={`max-w-[75%] rounded-2xl px-3.5 py-2 text-sm leading-relaxed ${
                    m.autor === "user"
                      ? "rounded-br-sm bg-indigo-600 text-white"
                      : "rounded-bl-sm bg-white text-slate-800 shadow-sm"
                  }`}
                >
                  {m.texto}
                </div>
                {m.autor === "user" && (
                  <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-slate-200 text-slate-600">
                    <User className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}
            {carregando && (
              <div className="flex items-end gap-2">
                <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-indigo-100 text-indigo-600">
                  <Bot className="h-4 w-4" />
                </div>
                <div className="flex items-center gap-1 rounded-2xl rounded-bl-sm bg-white px-4 py-3 shadow-sm">
                  <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                  <span className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
                </div>
              </div>
            )}
          </div>

          {/* Sugestões */}
          <div className="flex flex-wrap gap-1.5 border-t border-border bg-white px-3 py-2">
            {SUGESTOES.map((s) => (
              <button
                key={s}
                onClick={() => enviar(s)}
                disabled={carregando}
                className="rounded-full border border-slate-200 bg-slate-50 px-2.5 py-1 text-[11px] text-slate-700 transition hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-700 disabled:opacity-50"
              >
                {s}
              </button>
            ))}
          </div>

          {/* Input */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              enviar(input);
            }}
            className="flex items-center gap-2 border-t border-border bg-white px-3 py-2.5"
          >
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Digite sua mensagem..."
              className="flex-1 rounded-full border border-slate-200 bg-slate-50 px-4 py-2 text-sm outline-none placeholder:text-slate-400 focus:border-indigo-400 focus:bg-white"
            />
            <button
              type="submit"
              disabled={carregando || !input.trim()}
              aria-label="Enviar"
              className="flex h-9 w-9 items-center justify-center rounded-full bg-indigo-600 text-white transition hover:bg-indigo-700 disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
}

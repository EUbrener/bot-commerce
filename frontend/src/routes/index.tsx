import { createFileRoute } from "@tanstack/react-router";
import { useMemo, useState } from "react";
import {
  ShoppingCart,
  Search,
  X,
  Plus,
  Minus,
  Trash2,
  CheckCircle2,
  Zap,
} from "lucide-react";

import heroBanner from "@/assets/hero-banner.jpg";
import prodPhone from "@/assets/prod-phone.jpg";
import prodHeadphones from "@/assets/prod-headphones.jpg";
import prodWatch from "@/assets/prod-watch.jpg";
import prodEarbuds from "@/assets/prod-earbuds.jpg";
import prodSpeaker from "@/assets/prod-speaker.jpg";
import prodCharger from "@/assets/prod-charger.jpg";
import { Chatbot } from "@/components/Chatbot";

export const Route = createFileRoute("/")({
  component: Home,
  head: () => ({
    meta: [
      { title: "GadgetBR — Eletrônicos e Gadgets" },
      {
        name: "description",
        content:
          "Loja brasileira de eletrônicos e gadgets. Celulares, áudio e acessórios com entrega rápida.",
      },
    ],
  }),
});

interface Produto {
  id: number;
  nome: string;
  categoria: "Celulares" | "Áudio" | "Acessórios";
  preco: number;
  imagem: string;
}

const PRODUTOS: Produto[] = [
  { id: 1, nome: "Smartphone Nova X Pro", categoria: "Celulares", preco: 3499.9, imagem: prodPhone },
  { id: 2, nome: "Headphone Sonic HD", categoria: "Áudio", preco: 899.0, imagem: prodHeadphones },
  { id: 3, nome: "Smartwatch Pulse S2", categoria: "Acessórios", preco: 1299.0, imagem: prodWatch },
  { id: 4, nome: "Fones Air Buds Pro", categoria: "Áudio", preco: 649.9, imagem: prodEarbuds },
  { id: 5, nome: "Caixa de Som Boom Mini", categoria: "Áudio", preco: 429.0, imagem: prodSpeaker },
  { id: 6, nome: "Carregador Turbo 65W", categoria: "Acessórios", preco: 189.9, imagem: prodCharger },
];

const brl = (n: number) =>
  n.toLocaleString("pt-BR", { style: "currency", currency: "BRL" });

interface ItemCarrinho extends Produto {
  qtd: number;
}

function Home() {
  const [busca, setBusca] = useState("");
  const [carrinho, setCarrinho] = useState<ItemCarrinho[]>([]);
  const [drawerAberto, setDrawerAberto] = useState(false);
  const [pedidoModal, setPedidoModal] = useState<string | null>(null);

  const filtrados = useMemo(
    () =>
      PRODUTOS.filter(
        (p) =>
          p.nome.toLowerCase().includes(busca.toLowerCase()) ||
          p.categoria.toLowerCase().includes(busca.toLowerCase()),
      ),
    [busca],
  );

  const totalItens = carrinho.reduce((s, i) => s + i.qtd, 0);
  const totalPreco = carrinho.reduce((s, i) => s + i.qtd * i.preco, 0);

  const adicionar = (p: Produto) => {
    setCarrinho((c) => {
      const ex = c.find((i) => i.id === p.id);
      if (ex) return c.map((i) => (i.id === p.id ? { ...i, qtd: i.qtd + 1 } : i));
      return [...c, { ...p, qtd: 1 }];
    });
    setDrawerAberto(true);
  };

  const alterarQtd = (id: number, delta: number) => {
    setCarrinho((c) =>
      c
        .map((i) => (i.id === id ? { ...i, qtd: i.qtd + delta } : i))
        .filter((i) => i.qtd > 0),
    );
  };

  const remover = (id: number) =>
    setCarrinho((c) => c.filter((i) => i.id !== id));

  const finalizar = () => {
    const num = "PED-" + Math.floor(100000 + Math.random() * 900000);
    setPedidoModal(num);
    setCarrinho([]);
    setDrawerAberto(false);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {/* Header */}
      <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3 sm:px-6">
          <a href="/" className="flex items-center gap-2">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-indigo-600 text-white">
              <Zap className="h-5 w-5" />
            </div>
            <span className="text-lg font-bold tracking-tight">
              Gadget<span className="text-indigo-600">BR</span>
            </span>
          </a>

          <div className="relative ml-auto hidden max-w-md flex-1 sm:block">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar produtos, categorias..."
              className="w-full rounded-full border border-slate-200 bg-slate-50 py-2 pl-10 pr-4 text-sm outline-none focus:border-indigo-400 focus:bg-white"
            />
          </div>

          <button
            onClick={() => setDrawerAberto(true)}
            className="relative ml-auto flex h-10 w-10 items-center justify-center rounded-full bg-slate-100 hover:bg-slate-200 sm:ml-0"
            aria-label="Abrir carrinho"
          >
            <ShoppingCart className="h-5 w-5" />
            {totalItens > 0 && (
              <span className="absolute -right-1 -top-1 flex h-5 min-w-5 items-center justify-center rounded-full bg-indigo-600 px-1 text-[11px] font-semibold text-white">
                {totalItens}
              </span>
            )}
          </button>
        </div>

        {/* Busca mobile */}
        <div className="border-t border-slate-100 px-4 py-2 sm:hidden">
          <div className="relative">
            <Search className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
            <input
              value={busca}
              onChange={(e) => setBusca(e.target.value)}
              placeholder="Buscar produtos..."
              className="w-full rounded-full border border-slate-200 bg-slate-50 py-2 pl-10 pr-4 text-sm outline-none focus:border-indigo-400 focus:bg-white"
            />
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-10">
        <div className="relative overflow-hidden rounded-3xl">
          <img
            src={heroBanner}
            alt="Banner de gadgets"
            width={1600}
            height={700}
            className="h-56 w-full object-cover sm:h-80 md:h-96"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-slate-950/90 via-slate-950/60 to-transparent" />
          <div className="absolute inset-0 flex flex-col justify-center gap-3 px-6 sm:px-12">
            <span className="w-fit rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-white backdrop-blur">
              Novidades da semana
            </span>
            <h1 className="max-w-lg text-3xl font-bold leading-tight text-white sm:text-5xl">
              Tecnologia que <span className="text-indigo-400">move você</span>
            </h1>
            <p className="max-w-md text-sm text-slate-200 sm:text-base">
              Os melhores gadgets com entrega rápida para todo o Brasil.
              Parcele em até 12x sem juros.
            </p>
            <a
              href="#produtos"
              className="w-fit rounded-full bg-white px-5 py-2.5 text-sm font-semibold text-slate-900 shadow-lg transition hover:bg-slate-100"
            >
              Ver produtos
            </a>
          </div>
        </div>
      </section>

      {/* Produtos */}
      <section id="produtos" className="mx-auto max-w-7xl px-4 pb-16 sm:px-6">
        <div className="mb-6 flex items-end justify-between">
          <div>
            <h2 className="text-2xl font-bold tracking-tight sm:text-3xl">
              Produtos em destaque
            </h2>
            <p className="text-sm text-slate-500">
              {filtrados.length}{" "}
              {filtrados.length === 1 ? "produto encontrado" : "produtos encontrados"}
            </p>
          </div>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {filtrados.map((p) => (
            <article
              key={p.id}
              className="group flex flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white transition hover:-translate-y-0.5 hover:shadow-lg"
            >
              <div className="aspect-square overflow-hidden bg-slate-100">
                <img
                  src={p.imagem}
                  alt={p.nome}
                  loading="lazy"
                  width={800}
                  height={800}
                  className="h-full w-full object-cover transition duration-500 group-hover:scale-105"
                />
              </div>
              <div className="flex flex-1 flex-col gap-3 p-4">
                <span className="w-fit rounded-full bg-indigo-50 px-2.5 py-0.5 text-[11px] font-medium text-indigo-700">
                  {p.categoria}
                </span>
                <h3 className="font-semibold leading-snug">{p.nome}</h3>
                <div className="mt-auto flex items-end justify-between gap-2">
                  <div>
                    <p className="text-xs text-slate-500">à vista no Pix</p>
                    <p className="text-lg font-bold text-slate-900">
                      {brl(p.preco)}
                    </p>
                  </div>
                  <button
                    onClick={() => adicionar(p)}
                    className="rounded-full bg-slate-900 px-4 py-2 text-xs font-semibold text-white transition hover:bg-indigo-600"
                  >
                    Adicionar
                  </button>
                </div>
              </div>
            </article>
          ))}
        </div>

        {filtrados.length === 0 && (
          <div className="rounded-2xl border border-dashed border-slate-300 py-16 text-center text-slate-500">
            Nenhum produto encontrado para "{busca}".
          </div>
        )}
      </section>

      <footer className="border-t border-slate-200 bg-white py-8 text-center text-xs text-slate-500">
        © {new Date().getFullYear()} GadgetBR. Todos os direitos reservados.
      </footer>

      {/* Drawer Carrinho */}
      {drawerAberto && (
        <div className="fixed inset-0 z-40">
          <div
            className="absolute inset-0 bg-slate-950/40 animate-fade-in"
            onClick={() => setDrawerAberto(false)}
          />
          <aside className="absolute right-0 top-0 flex h-full w-full max-w-md animate-slide-in-right flex-col bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-200 px-5 py-4">
              <h3 className="text-lg font-semibold">Seu carrinho</h3>
              <button
                onClick={() => setDrawerAberto(false)}
                aria-label="Fechar"
                className="rounded-md p-1 hover:bg-slate-100"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="flex-1 overflow-y-auto px-5 py-4">
              {carrinho.length === 0 ? (
                <div className="flex h-full flex-col items-center justify-center text-center text-slate-500">
                  <ShoppingCart className="mb-3 h-10 w-10 text-slate-300" />
                  <p className="font-medium">Carrinho vazio</p>
                  <p className="text-xs">Adicione produtos para continuar.</p>
                </div>
              ) : (
                <ul className="space-y-4">
                  {carrinho.map((i) => (
                    <li key={i.id} className="flex gap-3">
                      <img
                        src={i.imagem}
                        alt=""
                        className="h-20 w-20 shrink-0 rounded-lg object-cover"
                      />
                      <div className="flex flex-1 flex-col">
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-sm font-semibold leading-tight">
                            {i.nome}
                          </p>
                          <button
                            onClick={() => remover(i.id)}
                            aria-label="Remover"
                            className="text-slate-400 hover:text-red-500"
                          >
                            <Trash2 className="h-4 w-4" />
                          </button>
                        </div>
                        <p className="text-xs text-slate-500">{i.categoria}</p>
                        <div className="mt-auto flex items-center justify-between">
                          <div className="flex items-center gap-1 rounded-full border border-slate-200">
                            <button
                              onClick={() => alterarQtd(i.id, -1)}
                              className="flex h-7 w-7 items-center justify-center rounded-full hover:bg-slate-100"
                              aria-label="Diminuir"
                            >
                              <Minus className="h-3.5 w-3.5" />
                            </button>
                            <span className="w-6 text-center text-sm font-medium">
                              {i.qtd}
                            </span>
                            <button
                              onClick={() => alterarQtd(i.id, 1)}
                              className="flex h-7 w-7 items-center justify-center rounded-full hover:bg-slate-100"
                              aria-label="Aumentar"
                            >
                              <Plus className="h-3.5 w-3.5" />
                            </button>
                          </div>
                          <p className="text-sm font-bold">
                            {brl(i.qtd * i.preco)}
                          </p>
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>

            {carrinho.length > 0 && (
              <div className="border-t border-slate-200 bg-slate-50 px-5 py-4">
                <div className="mb-3 flex items-center justify-between">
                  <span className="text-sm text-slate-600">Total</span>
                  <span className="text-xl font-bold">{brl(totalPreco)}</span>
                </div>
                <button
                  onClick={finalizar}
                  className="w-full rounded-full bg-indigo-600 py-3 text-sm font-semibold text-white transition hover:bg-indigo-700"
                >
                  Finalizar compra
                </button>
              </div>
            )}
          </aside>
        </div>
      )}

      {/* Modal sucesso */}
      {pedidoModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center px-4">
          <div
            className="absolute inset-0 bg-slate-950/50 animate-fade-in"
            onClick={() => setPedidoModal(null)}
          />
          <div className="relative w-full max-w-sm animate-scale-in rounded-2xl bg-white p-6 text-center shadow-2xl">
            <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-green-100 text-green-600">
              <CheckCircle2 className="h-8 w-8" />
            </div>
            <h3 className="text-xl font-bold">Pedido confirmado!</h3>
            <p className="mt-1 text-sm text-slate-500">
              Recebemos seu pedido e ele já está em processamento.
            </p>
            <div className="my-5 rounded-xl border border-dashed border-slate-300 bg-slate-50 py-3">
              <p className="text-xs text-slate-500">Número do pedido</p>
              <p className="text-lg font-bold tracking-wide text-indigo-600">
                {pedidoModal}
              </p>
            </div>
            <button
              onClick={() => setPedidoModal(null)}
              className="w-full rounded-full bg-slate-900 py-2.5 text-sm font-semibold text-white hover:bg-slate-800"
            >
              Continuar comprando
            </button>
          </div>
        </div>
      )}

      <Chatbot />
    </div>
  );
}

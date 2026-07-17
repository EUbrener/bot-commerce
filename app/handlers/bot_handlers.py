import random
from app.data.mock_data import MOCK_PEDIDOS

def handler_saudacao() -> str:
    """Handler para saudações."""
    respostas = [
        "Olá! 👋 Sou o assistente virtual da loja. Como posso ajudar você hoje?",
        "Oi! Bem-vindo ao atendimento. Em que posso ajudar?",
        "Olá! Estou aqui para ajudar. O que você precisa?"
    ]
    return random.choice(respostas)

def handler_despedida() -> str:
    """Handler para despedidas."""
    respostas = [
        "Obrigado pelo contato! 😊 Tenha um ótimo dia!",
        "Até logo! Se precisar de mais ajuda, é só chamar.",
        "Foi um prazer ajudar! Volte sempre. 👋"
    ]
    return random.choice(respostas)

def handler_fallback() -> str:
    """Handler para mensagens não compreendidas."""
    return """Desculpe, não entendi sua mensagem. 🤔

Posso ajudar com:
• Rastreamento de pedidos
• Devolução e troca
• Formas de pagamento
• Dúvidas frequentes

Gostaria de falar com um atendente humano?"""

def handler_devolucao(entidades: dict) -> str:
    """Handler para solicitações de devolução."""
    resposta = """📦 **Política de Devolução**

Você pode solicitar devolução em até 7 dias após o recebimento.

**Como fazer:**
1. Acesse "Meus Pedidos" no site ou app
2. Selecione o produto
3. Clique em "Solicitar Devolução"
4. Escolha o motivo e aguarde instruções

A coleta é gratuita e o reembolso é processado em até 10 dias úteis."""

    # Adicionar info sobre data se extraída
    if entidades.get('datas', {}).get('validos'):
        data = entidades['datas']['validos'][0]
        resposta += f"\n\n📅 Vi que você mencionou a data {data}. Se a compra foi feita há mais de 7 dias, entre em contato para verificarmos."

    return resposta

def consultar_pedido_mock(numero_pedido: str) -> str:
    """Consulta pedido no mock de dados."""
    if numero_pedido in MOCK_PEDIDOS:
        info = MOCK_PEDIDOS[numero_pedido]
        status = info.get('status', 'Desconhecido')

        resposta = f"📦 **Pedido {numero_pedido}**\n\n"
        resposta += f"**Status:** {status}\n"

        if 'previsao' in info:
            resposta += f"**Previsão de entrega:** {info['previsao']}\n"
        if 'transportadora' in info:
            resposta += f"**Transportadora:** {info['transportadora']}\n"
        if 'data_entrega' in info:
            resposta += f"**Data de entrega:** {info['data_entrega']}\n"
        if 'recebedor' in info:
            resposta += f"**Recebido por:** {info['recebedor']}\n"
        if 'expira' in info:
            resposta += f"**⚠️ Pagamento expira em:** {info['expira']}\n"

        return resposta
    else:
        return f"❌ Pedido {numero_pedido} não encontrado em nossa base. Verifique o número e tente novamente."

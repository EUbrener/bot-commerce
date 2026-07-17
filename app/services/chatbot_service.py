import logging
from collections import defaultdict
from typing import Dict, Any, List, Optional, Tuple
import numpy as np

from app.nlp.classifier import classificar_com_confianca_calibrada
from app.nlp.entities import extrair_e_validar_entidades
from app.nlp.faq import buscar_faq_multinivel
from app.nlp.sentiment import analisar_sentimento_mensagem
from app.handlers.bot_handlers import (
    handler_saudacao,
    handler_despedida,
    handler_fallback,
    handler_devolucao,
    consultar_pedido_mock
)

logger = logging.getLogger(__name__)

# Armazena em memória as estatísticas de analytics
ANALYTICS = {
    'total_mensagens': 0,
    'intencoes': defaultdict(int),
    'sentimentos': {'positivo': 0, 'negativo': 0, 'neutro': 0},
    'entidades_extraidas': defaultdict(int),
    'faq_matches': {'tfidf': 0, 'bigrama': 0, 'sugestoes': 0},
    'escalacoes_humano': 0,
    'historico_confianca': []
}

def registrar_analytics(resultado: Dict[str, Any], sentimento_label: str):
    """Registra as métricas da interação no analytics global."""
    try:
        ANALYTICS['total_mensagens'] += 1
        ANALYTICS['intencoes'][resultado['intencao']] += 1
        ANALYTICS['historico_confianca'].append(resultado['confianca'])
        ANALYTICS['sentimentos'][sentimento_label] += 1

        if resultado.get('requer_humano'):
            ANALYTICS['escalacoes_humano'] += 1

        if resultado.get('nivel_busca'):
            ANALYTICS['faq_matches'][resultado['nivel_busca']] += 1

        # Contar entidades
        for tipo, dados in resultado.get('entidades', {}).items():
            ANALYTICS['entidades_extraidas'][tipo] += len(dados.get('validos', []))
    except Exception as e:
        logger.error(f"Erro ao registrar analytics: {e}")

def obter_analytics() -> Dict[str, Any]:
    """Retorna um snapshot serializável das métricas de analytics."""
    media_conf = 0.0
    if ANALYTICS['historico_confianca']:
        media_conf = float(np.mean(ANALYTICS['historico_confianca']))

    return {
        'total_mensagens': ANALYTICS['total_mensagens'],
        'escalacoes_humano': ANALYTICS['escalacoes_humano'],
        'confianca_media': media_conf,
        'intencoes': dict(ANALYTICS['intencoes']),
        'sentimentos': dict(ANALYTICS['sentimentos']),
        'faq_matches': dict(ANALYTICS['faq_matches']),
        'entidades_extraidas': dict(ANALYTICS['entidades_extraidas'])
    }

def processar_mensagem(mensagem: str, historico: Optional[List[Tuple[str, str]]] = None) -> Dict[str, Any]:
    """
    Pipeline principal do chatbot.

    Args:
        mensagem: Mensagem do usuário
        historico: Histórico de mensagens anteriores (opcional, mantido para retrocompatibilidade)

    Returns:
        Dicionário com resposta, intenção, confiança, entidades e flags
    """
    # 1. Identificar a intenção e a confiança calibrada
    intencao, confianca, requer_humano = classificar_com_confianca_calibrada(mensagem)

    # 2. Extrair e validar entidades
    entidades = extrair_e_validar_entidades(mensagem)

    # 3. Executar busca FAQ multi-nível (para fins de preenchimento de nível de busca)
    resposta_faq, score_faq, nivel_busca = buscar_faq_multinivel(mensagem)

    # 4. Roteamento baseado na intenção
    if intencao == 'saudacao':
        resposta = handler_saudacao()
    elif intencao == 'despedida':
        resposta = handler_despedida()
    elif intencao == 'rastreamento':
        # Se houver um código de pedido válido, consulta seu status
        valid_orders = entidades.get('pedidos', {}).get('validos', [])
        if valid_orders:
            resposta = consultar_pedido_mock(valid_orders[0])
        else:
            resposta = "Para rastrear, por favor informe o número do pedido (ex: PED-123456 ou ORD-123456)."
    elif intencao == 'devolucao':
        resposta = handler_devolucao(entidades)
    elif intencao == 'reclamacao':
        # Sempre requer humano
        requer_humano = True
        valores_validos = entidades.get('valores', {}).get('validos', [])
        valor_mencionado = f" sobre o valor de {valores_validos[0]}" if valores_validos else ""
        resposta = f"Sinto muito pelo ocorrido{valor_mencionado}. Estou transferindo você para um atendente humano agora."
    elif intencao in ['faq', 'pagamento']:
        resposta = resposta_faq
    else:
        # Caso incerto
        resposta = handler_fallback()
        requer_humano = True

    # 5. Analisar o sentimento da mensagem
    analise_sentimento = analisar_sentimento_mensagem(mensagem)
    sentimento_label = analise_sentimento['sentimento']

    # Criar dicionário de resultado
    resultado = {
        'resposta': resposta,
        'intencao': intencao,
        'confianca': confianca,
        'entidades': entidades,
        'requer_humano': requer_humano,
        'nivel_busca': nivel_busca if intencao in ['faq', 'pagamento', 'incerto'] else None,
        'sentimento': analise_sentimento
    }

    # 6. Registrar analytics
    registrar_analytics(resultado, sentimento_label)

    # Adicionar tag de transferência se requer atendimento humano
    if requer_humano:
        resultado['resposta'] += "\n\n🔴 *[Transferindo para atendente humano...]*"

    return resultado

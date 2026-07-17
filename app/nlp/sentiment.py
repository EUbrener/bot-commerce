import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Cache para o pipeline de análise de sentimento
_sentiment_analyzer = None
_bert_disponivel = None

def get_sentiment_analyzer():
    """Inicializa e retorna o pipeline de análise de sentimento do HuggingFace, armazenando em cache para chamadas posteriores."""
    global _sentiment_analyzer, _bert_disponivel
    if _bert_disponivel is False:
        return None

    if _sentiment_analyzer is None:
        try:
            from transformers import pipeline
            # nlptown/bert-base-multilingual-uncased-sentiment predicts 1 to 5 stars
            _sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="nlptown/bert-base-multilingual-uncased-sentiment",
                device=-1  # Força CPU para evitar problemas de dependência CUDA durante implantações simples
            )
            _bert_disponivel = True
            logger.info("Modelo de análise de sentimento BERT carregado com sucesso!")
        except Exception as e:
            logger.warning(f"Não foi possível carregar o modelo de sentimento BERT: {e}. Voltando para análise de sentimento baseada em palavras-chave.")
            _sentiment_analyzer = None
            _bert_disponivel = False

    return _sentiment_analyzer

def analisar_sentimento_mensagem(texto: str) -> Dict[str, Any]:
    """
    Analisa o sentimento de uma mensagem usando BERT ou um fallback baseado em palavras-chave.

    Args:
        texto: A mensagem a ser analisada.

    Returns:
        Um dicionário contendo 'sentimento', 'confianca' e 'estrelas'.
    """
    analyzer = get_sentiment_analyzer()
    if analyzer is not None:
        try:
            # Previsão usando o pipeline do HuggingFace, limitando o texto a 512 caracteres
            result = analyzer(texto[:512])[0]
            label = result['label']  # ex: '1 star' ou '5 stars'
            score = float(result['score'])

            # Converte 1-5 estrelas para positivo/negativo/neutro
            stars = int(label.split()[0])
            if stars >= 4:
                sentimento = 'positivo'
            elif stars <= 2:
                sentimento = 'negativo'
            else:
                sentimento = 'neutro'

            return {'sentimento': sentimento, 'confianca': score, 'estrelas': stars}
        except Exception as e:
            logger.error(f"Erro ao prever com BERT: {e}. Voltando para palavras-chave.")

    # Fallback: Análise de sentimento baseada em palavras-chave
    texto_lower = texto.lower()
    palavras_positivas = ['bom', 'ótimo', 'excelente', 'obrigado', 'parabéns', 'adorei', 'amei', 'perfeito']
    palavras_negativas = ['ruim', 'péssimo', 'horrível', 'quebrado', 'defeito', 'reclamar', 'absurdo', 'nunca']

    pos = sum(1 for p in palavras_positivas if p in texto_lower)
    neg = sum(1 for p in palavras_negativas if p in texto_lower)

    if pos > neg:
        return {'sentimento': 'positivo', 'confianca': 0.7, 'estrelas': 4}
    elif neg > pos:
        return {'sentimento': 'negativo', 'confianca': 0.7, 'estrelas': 2}
    else:
        return {'sentimento': 'neutro', 'confianca': 0.5, 'estrelas': 3}

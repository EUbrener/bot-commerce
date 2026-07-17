import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# Cache for the sentiment analyzer pipeline
_sentiment_analyzer = None
_bert_disponivel = None

def get_sentiment_analyzer():
    """Initializes and returns the HuggingFace sentiment pipeline, caching it for subsequent calls."""
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
                device=-1  # Force CPU to avoid CUDA dependency issues during simple deployments
            )
            _bert_disponivel = True
            logger.info("BERT sentiment analyzer model loaded successfully!")
        except Exception as e:
            logger.warning(f"BERT sentiment model could not be loaded: {e}. Falling back to keyword-based sentiment analysis.")
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
            # Predict using HuggingFace pipeline, limiting text to 512 characters
            result = analyzer(texto[:512])[0]
            label = result['label']  # e.g., '1 star' or '5 stars'
            score = float(result['score'])

            # Convert 1-5 stars to positive/negative/neutro
            stars = int(label.split()[0])
            if stars >= 4:
                sentimento = 'positivo'
            elif stars <= 2:
                sentimento = 'negativo'
            else:
                sentimento = 'neutro'

            return {'sentimento': sentimento, 'confianca': score, 'estrelas': stars}
        except Exception as e:
            logger.error(f"Error predicting with BERT: {e}. Falling back to keywords.")

    # Fallback: Keyword-based sentiment analysis
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

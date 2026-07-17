import joblib
from typing import Tuple, Optional, List
from nltk import bigrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app import config
from app.nlp.preprocessor import preprocessar_texto_configuravel
from app.data.faq_data import FAQ_PERGUNTAS, FAQ_RESPOSTAS

# Variáveis globais para armazenar os modelos de FAQ
_vetorizador_faq = None
_modelo_bigrama_faq = None

def load_faq_models():
    """Carrega o vetorizador e os modelos de bigramas do FAQ, caso ainda não estejam carregados."""
    global _vetorizador_faq, _modelo_bigrama_faq
    if _vetorizador_faq is None:
        if config.VECTORIZER_FAQ_PATH.exists():
            _vetorizador_faq = joblib.load(config.VECTORIZER_FAQ_PATH)
        else:
            raise FileNotFoundError(
                "Arquivo do vetorizador do FAQ não encontrado. Por favor, execute 'python train.py'."
            )
    if _modelo_bigrama_faq is None:
        if config.BIGRAM_FAQ_PATH.exists():
            _modelo_bigrama_faq = joblib.load(config.BIGRAM_FAQ_PATH)
        else:
            # Fallback para bigramas dinâmicos ou dicionário vazio se o treinamento não ocorreu
            _modelo_bigrama_faq = {}
    return _vetorizador_faq, _modelo_bigrama_faq

def vetorizar_texto(texto: str, vetorizador: TfidfVectorizer):
    return vetorizador.transform([texto])

def calcular_similaridade(vetor1, vetor2) -> float:
    return float(cosine_similarity(vetor1, vetor2)[0, 0])

def buscar_faq(
    pergunta: str,
    perguntas_faq: List[str],
    respostas_faq: List[str],
    vetorizador: TfidfVectorizer,
    threshold: float = config.THRESHOLD_TFIDF
) -> Tuple[Optional[str], float]:
    """
    Busca uma pergunta no FAQ calculando a similaridade TF-IDF.
    """
    vetor_pergunta = vetorizar_texto(pergunta, vetorizador)
    resposta_mais_similar = None
    maior_similaridade = 0.0

    for pergunta_faq, resposta_faq in zip(perguntas_faq, respostas_faq):
        vetor_faq = vetorizar_texto(pergunta_faq, vetorizador)
        similaridade = calcular_similaridade(vetor_pergunta, vetor_faq)
        if similaridade >= threshold and similaridade > maior_similaridade:
            resposta_mais_similar = resposta_faq
            maior_similaridade = similaridade

    return resposta_mais_similar, maior_similaridade

def buscar_faq_multinivel(
    pergunta: str,
    perguntas_faq: List[str] = FAQ_PERGUNTAS,
    respostas_faq: List[str] = FAQ_RESPOSTAS,
    vetorizador_tfidf: Optional[TfidfVectorizer] = None,
    modelo_bigrama: Optional[dict] = None
) -> Tuple[Optional[str], float, str]:
    """
    Busca no FAQ com múltiplos níveis.

    Níveis:
    1. TF-IDF (threshold 0.7) - match direto
    2. Bigramas (threshold 0.3) - fallback
    3. Sugestões top-3 - quando nada encontrado

    Returns:
        Tupla (resultado, score, nivel)
        - nivel: 'tfidf', 'bigrama', ou 'sugestoes'
    """
    if vetorizador_tfidf is None:
        vetorizador_tfidf, _ = load_faq_models()

    # Nível 1: Match direto TF-IDF
    resultado_tfidf, score_tfidf = buscar_faq(
        pergunta, perguntas_faq, respostas_faq, vetorizador_tfidf, threshold=config.THRESHOLD_TFIDF
    )
    if resultado_tfidf and score_tfidf >= config.THRESHOLD_TFIDF:
        return resultado_tfidf, score_tfidf, 'tfidf'

    # Nível 2: Fallback usando interseção de bigramas
    pergunta_proc = preprocessar_texto_configuravel(pergunta, aplicar_stemming=False)
    tokens_p = pergunta_proc.split()
    bigramas_p = set(bigrams(tokens_p))

    melhor_score_bigrama = 0.0
    melhor_resposta_bigrama = None

    if bigramas_p:
        for f_pergunta, f_resposta in zip(perguntas_faq, respostas_faq):
            f_proc = preprocessar_texto_configuravel(f_pergunta, aplicar_stemming=False)
            tokens_f = f_proc.split()
            bigramas_f = set(bigrams(tokens_f))

            if not bigramas_f:
                continue

            comuns = len(bigramas_p.intersection(bigramas_f))
            score = comuns / max(len(bigramas_p), len(bigramas_f))

            if score > melhor_score_bigrama:
                melhor_score_bigrama = score
                melhor_resposta_bigrama = f_resposta

    if melhor_score_bigrama >= config.THRESHOLD_BIGRAMA:
        return melhor_resposta_bigrama, melhor_score_bigrama, 'bigrama'

    # Nível 3: Sugestões baseadas nas top 3 perguntas mais similares
    vetor_p = vetorizador_tfidf.transform([pergunta])
    vetores_faq = vetorizador_tfidf.transform(perguntas_faq)
    similaridades = cosine_similarity(vetor_p, vetores_faq).flatten()

    top_indices = similaridades.argsort()[-3:][::-1]
    sugestoes = [perguntas_faq[i] for i in top_indices]

    msg_sugestao = "Não encontrei uma resposta exata. Você quis dizer: " + ", ".join(
        [f"{i+1}. {s}" for i, s in enumerate(sugestoes)]
    )

    return msg_sugestao, float(similaridades[top_indices[0]]), 'sugestoes'

import joblib
from typing import Tuple, Optional
from app import config

# Global variables to store the loaded models
_classificador = None
_vetorizador = None

def load_classifier():
    """Loads the classifier and vectorizer models if they are not already loaded."""
    global _classificador, _vetorizador
    if _classificador is None or _vetorizador is None:
        if config.CLASSIFIER_INTENT_PATH.exists() and config.VECTORIZER_INTENT_PATH.exists():
            _classificador = joblib.load(config.CLASSIFIER_INTENT_PATH)
            _vetorizador = joblib.load(config.VECTORIZER_INTENT_PATH)
        else:
            raise FileNotFoundError(
                "Model files not found. Please run 'python train.py' to train and persist models."
            )
    return _classificador, _vetorizador

def classificar_com_confianca_calibrada(
    texto: str,
    classificador=None,
    vetorizador=None,
    threshold: float = config.THRESHOLD_CONFIANCA
) -> Tuple[str, float, bool]:
    """
    Classifica intenção com indicação de escalação.

    Args:
        texto: Texto para classificar
        classificador: LogisticRegression treinado (opcional, se None carrega o padrão)
        vetorizador: TfidfVectorizer treinado (opcional, se None carrega o padrão)
        threshold: Limiar de confiança (default config.THRESHOLD_CONFIANCA)

    Returns:
        Tupla (intencao, confianca, requer_humano)
    """
    if classificador is None or vetorizador is None:
        classificador, vetorizador = load_classifier()

    # 1. Vetorização: Transforma o texto de entrada em uma representação numérica
    vetor_texto = vetorizador.transform([texto])

    # 2. Predição de Classe: O modelo identifica a melhor intenção
    intencao = classificador.predict(vetor_texto)[0]

    # 3. Cálculo de Probabilidade: Obtém a confiança do modelo para a classe escolhida
    classes_list = classificador.classes_.tolist()
    class_idx = classes_list.index(intencao)
    confianca = float(classificador.predict_proba(vetor_texto)[0, class_idx])

    # Inicializa a flag de atendimento humano como falso
    requer_humano = False

    # 4. Lógica de Threshold: Se a confiança for menor que o limite definido, marca como incerto
    if confianca < threshold:
        intencao = 'incerto'
        requer_humano = True

    # 5. Regra de Negócio: Reclamações, devoluções e rastreamento requerem atendimento humano
    elif intencao == 'reclamacao':
        requer_humano = True
    elif intencao == 'devolucao':
        requer_humano = True
    elif intencao == 'rastreamento':
        requer_humano = True

    return intencao, confianca, requer_humano

import os
from pathlib import Path

# Paths
APP_DIR = Path(__file__).resolve().parent
ROOT_DIR = APP_DIR.parent
MODELS_DIR = ROOT_DIR / "models"

# Ensure models directory exists
MODELS_DIR.mkdir(parents=True, exist_ok=True)

# Path to trained model files
VECTORIZER_INTENT_PATH = MODELS_DIR / "vetorizador_intencoes.pkl"
CLASSIFIER_INTENT_PATH = MODELS_DIR / "classificador_intencoes.pkl"
VECTORIZER_FAQ_PATH = MODELS_DIR / "vetorizador_faq.pkl"
BIGRAM_FAQ_PATH = MODELS_DIR / "modelo_bigrama_faq.pkl"

# Reproducibility
SEED_AVALIACAO = 42

# TF-IDF Parameters
TFIDF_MAX_FEATURES = 500
TFIDF_NGRAM_RANGE = (1, 2)
TFIDF_MIN_DF = 1

# Classifier Parameters
SPLIT_TEST_SIZE = 0.2
SPLIT_RANDOM_STATE = 42
LR_MAX_ITER = 1000
LR_C = 2.0
LR_MULTI_CLASS = 'multinomial'

# System Thresholds
THRESHOLD_TFIDF = 0.7          # Level 1: TF-IDF direct match
THRESHOLD_BIGRAMA = 0.3        # Level 2: Bigram fallback
THRESHOLD_CONFIANCA = 0.6      # Q3: Threshold for intent confidence
THRESHOLD_HUMANO = 0.5         # Below this, request human intervention

# Regex Patterns (raw strings to avoid escape warnings)
REGEX_PEDIDO = r'(?:PED|ORD)-\d{5,10}|\b\d{6,10}\b'
REGEX_VALOR = r'R\$\s*\d{1,3}(?:\.\d{3})*(?:,\d{2})?'
REGEX_DATA = r'\d{2}[/-]\d{2}[/-]\d{4}'
REGEX_EMAIL = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
REGEX_TELEFONE = r'(?:\(\d{2}\)\s*)?\d{4,5}-?\d{4}|0800-?\d{3}-?\d{4}'

# Valid Brazilian Area Codes (DDDs)
DDDS_VALIDOS = {
    '11', '12', '13', '14', '15', '16', '17', '18', '19',  # SP
    '21', '22', '24',  # RJ
    '27', '28',  # ES
    '31', '32', '33', '34', '35', '37', '38',  # MG
    '41', '42', '43', '44', '45', '46',  # PR
    '47', '48', '49',  # SC
    '51', '53', '54', '55',  # RS
    '61',  # DF
    '62', '64',  # GO
    '63',  # TO
    '65', '66',  # MT
    '67',  # MS
    '68',  # AC
    '69',  # RO
    '71', '73', '74', '75', '77',  # BA
    '79',  # SE
    '81', '87',  # PE
    '82',  # AL
    '83',  # PB
    '84',  # RN
    '85', '88',  # CE
    '86', '89',  # PI
    '91', '93', '94',  # PA
    '92', '97',  # AM
    '95',  # RR
    '96',  # AP
    '98', '99'  # MA
}

import re
import unicodedata
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer

# Garantir que os recursos do NLTK estejam baixados
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('stemmers/rslp')
except LookupError:
    nltk.download('rslp', quiet=True)

def preprocessar_texto_configuravel(
    texto: str,
    remover_stopwords: bool = True,
    aplicar_stemming: bool = True,
    min_palavra_length: int = 2,
    normalizar_acentos: bool = False
) -> str:
    """
    Pré-processa texto com configurações flexíveis.

    Args:
        texto: Texto para processar
        remover_stopwords: Se True, remove stopwords
        aplicar_stemming: Se True, aplica stemming RSLP
        min_palavra_length: Tamanho mínimo de palavra
        normalizar_acentos: Se True, remove acentos

    Returns:
        Texto pré-processado (tokens unidos por espaço)
    """
    # 1. Converter para minúsculas
    texto = texto.lower()
    
    # 2. Remover URLs (http://, https://, www.)
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    
    # 3. Remover emails (padrões com @)
    texto = re.sub(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', '', texto)
    
    # 4. Remover números isolados
    texto = re.sub(r'\b\d+\b', '', texto)
    
    # 5. Remover pontuação
    texto = re.sub(r'[^\w\s]', '', texto)

    # 6. Se normalizar_acentos=True: remover acentos
    if normalizar_acentos:
        texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII')

    # 7. Tokenizar usando NLTK word_tokenize
    tokens = word_tokenize(texto)

    # 8. Manter apenas tokens alfabéticos
    tokens = [t for t in tokens if t.isalpha()]

    # 9. Se remover_stopwords=True: remover stopwords do NLTK português
    if remover_stopwords:
        stop_words = set(stopwords.words('portuguese'))
        tokens = [t for t in tokens if t not in stop_words]

    # 10. Filtrar palavras menores que min_palavra_length
    tokens = [t for t in tokens if len(t) >= min_palavra_length]

    # 11. Se aplicar_stemming=True: aplicar RSLP stemmer
    if aplicar_stemming:
        stemmer = RSLPStemmer()
        tokens = [stemmer.stem(t) for t in tokens]

    # 12. Retornar texto processado (tokens unidos por espaço)
    return ' '.join(tokens)

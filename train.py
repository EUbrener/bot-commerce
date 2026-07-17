import joblib
import random
import numpy as np
from collections import defaultdict
import nltk
from nltk.tokenize import word_tokenize
from nltk import bigrams
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

from app import config
from app.data.intent_data import INTENCOES_TEXTOS, INTENCOES_LABELS
from app.data.faq_data import FAQ_PERGUNTAS

# Ensure NLTK packages are downloaded
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)

def construir_modelo_bigrama(corpus):
    modelo = defaultdict(lambda: defaultdict(int))
    for texto in corpus:
        tokens = word_tokenize(texto.lower())
        tokens = [t for t in tokens if t.isalpha()]
        tokens = ['<s>'] + tokens + ['</s>']
        for w1, w2 in bigrams(tokens):
            modelo[w1][w2] += 1
    return {k: dict(v) for k, v in modelo.items()}

def train_and_persist():
    print("Iniciando treinamento dos modelos...")
    print("=" * 50)

    # 1. Configurar seeds para reprodutibilidade
    np.random.seed(config.SEED_AVALIACAO)
    random.seed(config.SEED_AVALIACAO)

    # 2. Vetorizador para Classificação de Intenções
    print("Treinando vetorizador de intenções...")
    vetorizador_intencoes = TfidfVectorizer(
        ngram_range=config.TFIDF_NGRAM_RANGE,
        max_features=config.TFIDF_MAX_FEATURES,
        min_df=config.TFIDF_MIN_DF,
        lowercase=True
    )

    X = vetorizador_intencoes.fit_transform(INTENCOES_TEXTOS)
    y = np.array(INTENCOES_LABELS)

    # Split para avaliação
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=config.SPLIT_TEST_SIZE,
        random_state=config.SPLIT_RANDOM_STATE,
        stratify=y
    )

    print(f"   Vetorizador de intenções: {len(vetorizador_intencoes.vocabulary_)} features")
    print(f"   Treino: {X_train.shape[0]} exemplos, Teste: {X_test.shape[0]} exemplos")

    # 3. Classificador de Intenções
    print("Treinando classificador de intenções (Regressão Logística)...")
    classificador_intencoes = LogisticRegression(
        max_iter=config.LR_MAX_ITER,
        random_state=config.SEED_AVALIACAO,
        C=config.LR_C,
        solver='lbfgs'
    )
    classificador_intencoes.fit(X_train, y_train)

    # Avaliar
    y_pred = classificador_intencoes.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f"   Acurácia: {acc:.2%}")
    print(f"   F1-macro: {f1:.2%}")

    # Treinar novamente no dataset completo para produção
    print("Refitando classificador no dataset completo...")
    classificador_intencoes_prod = LogisticRegression(
        max_iter=config.LR_MAX_ITER,
        random_state=config.SEED_AVALIACAO,
        C=config.LR_C,
        solver='lbfgs'
    )
    classificador_intencoes_prod.fit(X, y)

    # 4. Vetorizador para FAQ
    print("Treinando vetorizador de FAQ...")
    vetorizador_faq = TfidfVectorizer(
        ngram_range=config.TFIDF_NGRAM_RANGE,
        max_features=config.TFIDF_MAX_FEATURES,
        min_df=config.TFIDF_MIN_DF,
        lowercase=True
    )
    vetorizador_faq.fit(FAQ_PERGUNTAS)
    print(f"   Vetorizador de FAQ: {len(vetorizador_faq.vocabulary_)} features")

    # 5. Modelo de Bigramas para FAQ
    print("Construindo modelo de bigramas para FAQ...")
    modelo_bigrama_faq = construir_modelo_bigrama(FAQ_PERGUNTAS)
    print(f"   Modelo de bigramas: {len(modelo_bigrama_faq)} palavras iniciais")

    # 6. Salvar os modelos
    print(f"Salvando modelos em: {config.MODELS_DIR}")
    joblib.dump(vetorizador_intencoes, config.VECTORIZER_INTENT_PATH)
    joblib.dump(classificador_intencoes_prod, config.CLASSIFIER_INTENT_PATH)
    joblib.dump(vetorizador_faq, config.VECTORIZER_FAQ_PATH)
    joblib.dump(modelo_bigrama_faq, config.BIGRAM_FAQ_PATH)

    print("=" * 50)
    print("Todos os modelos foram treinados e persistidos com sucesso!")

if __name__ == "__main__":
    train_and_persist()

# 📊 Guia de Apresentação do Projeto: Chatbot E-commerce
Este documento serve como um roteiro e estrutura de slides para a apresentação do projeto. O foco principal é detalhar a arquitetura de Processamento de Linguagem Natural (PLN), a lógica de desenvolvimento do pipeline e o treinamento/validação dos modelos de Machine Learning.

---

## 🖥️ Slide 1: Introdução ao Projeto
* **Título do Slide**: Chatbot Inteligente de Atendimento para E-commerce
* **Subtítulo**: Arquitetura de Produção com Processamento de Linguagem Natural e Persistência de Modelos
* **Conteúdo**:
  * **Problema**: Atendimento ao cliente de e-commerce é repetitivo e necessita de respostas rápidas, mas requer triagem inteligente para casos complexos.
  * **Solução**: Um chatbot robusto em Python estruturado como API (FastAPI) consumido por uma interface de e-commerce responsiva.
  * **Destaque**: Integração completa de algoritmos clássicos de PLN (TF-IDF, Bigramas), classificadores lineares (Regressão Logística) e modelos de Deep Learning (Transformers/BERT).

---

## 🛠️ Slide 2: Arquitetura Geral do Pipeline
* **Título do Slide**: O Fluxo de Processamento de uma Mensagem
* **Visual**:
  ```
  Entrada do Usuário (Texto)
          │
          ▼
  [1] Pré-processamento Configurável (Limpeza e Normalização NLTK)
          │
          ▼
  [2] Extração & Validação de Entidades (Regex e Regras de Negócio)
          │
          ▼
  [3] Classificação de Intenções (Logistic Regression calibrado por Threshold)
          │
          ├────────► Se confiança < 0.60 ──► Intenção: "incerto" ──► Escalado Humano
          │
          ├────────► Se "reclamacao"/"devolucao" ──────────────────► Escalado Humano
          │
          ▼
  [4] Busca FAQ Multi-nível (TF-IDF ──► Fallback Bigramas ──► Sugestões Top 3)
          │
          ▼
  [5] Análise de Sentimento (BERT Multilingual em HuggingFace)
          │
          ▼
  Geração da Resposta + Registro em Analytics (Snapshot em tempo real)
  ```

---

## 🧹 Slide 3: Engenharia de Recursos – Pré-processamento
* **Título do Slide**: Engenharia de Pré-processamento Configurável
* **Conteúdo**:
  * Implementado no módulo [preprocessor.py](file:///c:/Users/Brener/Documents/projetos/bot-commerce/app/nlp/preprocessor.py).
  * **Pipeline de Limpeza**:
    1. **Lowercasing**: Padronização para minúsculas.
    2. **Remoção de Ruído**: Expressões Regulares para limpar URLs, endereços de email, números soltos e caracteres especiais/pontuações.
    3. **Normalização Opcional**: Remoção de acentuação gráfica portuguesa (`NFKD` unicodedata).
    4. **Tokenização**: Divisão em tokens de palavras através do `word_tokenize` do NLTK.
    5. **Filtragem de Stopwords**: Remoção de palavras vazias de significado (artigos, preposições) em português.
    6. **Stemming (RSLPStemmer)**: Redução de palavras ao seu radical básico (ex: *"comprando"*, *"comprei"*, *"compra"* ──► *"compr"*).

---

## 🎯 Slide 4: Classificador de Intenções
* **Título do Slide**: Classificador de Intenções com Confiança Calibrada
* **Conteúdo**:
  * **Dataset**: 280 queries de treino divididas em 7 classes balanceadas (`saudacao`, `despedida`, `rastreamento`, `devolucao`, `reclamacao`, `pagamento`, `faq`).
  * **Vetorização**: `TfidfVectorizer` (N-gramas de 1 a 2 palavras, máximo de 500 features).
  * **Modelo**: Regressão Logística (`LogisticRegression` da scikit-learn).
  * **Lógica de Calibração (Threshold)**:
    * Se a probabilidade máxima da classe predita (`predict_proba`) for menor que **0.60**, o bot assume que a intenção é `incerto` e marca o parâmetro `requer_humano=True`.
    * Regras de negócio forçam escalação humana automática para as categorias de `reclamacao`, `devolucao` e `rastreamento`.
  * **Resultados de Acurácia**: **78.57%** no conjunto de teste e **80%** de taxa de sucesso geral nos casos de regressão.

---

## 🔍 Slide 5: Busca Multinível no FAQ
* **Título do Slide**: Busca em FAQ com 3 Níveis de Fallback
* **Conteúdo**:
  * Desenvolvido para mitigar o problema de respostas vazias e guiar o cliente de forma fluida.
  * **Nível 1: TF-IDF Direto (Threshold 0.70)**
    * Vetorização da pergunta do usuário e cálculo da **Similaridade de Cosseno** contra as perguntas da base do FAQ.
    * Se similaridade $\ge$ 0.70, retorna a resposta exata.
  * **Nível 2: Fallback por Bigramas (Threshold 0.30)**
    * Extração de bigramas do texto pré-processado do usuário e das perguntas do FAQ.
    * Score calculado via interseção de conjuntos: $\text{score} = \frac{\text{bigramas comuns}}{\max(\text{bigramas user}, \text{bigramas faq})}$.
    * Se o score $\ge$ 0.30, responde com a pergunta correspondente.
  * **Nível 3: Sugestões Inteligentes (Top-3)**
    * Se nenhum critério for atingido, o bot calcula as top 3 perguntas mais próximas no espaço vetorial TF-IDF e gera a string: *"Você quis dizer: 1. X, 2. Y, 3. Z"*.

---

## 🏷️ Slide 6: Extração de Entidades e Validação
* **Título do Slide**: Extração de Informação Nomeada e Regex
* **Conteúdo**:
  * Responsável por extrair variáveis de contexto da conversa e validá-las antes de repassá-las às regras de negócios.
  * **Regras e Filtros aplicados**:
    * **Número do Pedido**: Expressão regular `(?:PED|ORD)-\d{5,10}`. Apenas dígitos após o traço de comprimento 5 a 10 são considerados válidos.
    * **Datas**: Formatos comuns `DD/MM/AAAA`. Validado se o ano está entre 2020 e 2030, e se a data não ultrapassa 1 ano no futuro.
    * **Valores Monetários**: Formato `R$ X,XX`. Validação de faixa de preço aceitável (entre R$ 0,00 e R$ 10.000,00).
    * **Email & Telefone**: Formatos básicos e DDDs nacionais válidos.

---

## 🎭 Slide 7: Análise de Sentimento (Transformers / BERT)
* **Título do Slide**: Inteligência de Sentimento com Deep Learning
* **Conteúdo**:
  * Utilização prática do modelo **BERT** para priorização de atendimento e análise qualitativa.
  * **Modelo**: `nlptown/bert-base-multilingual-uncased-sentiment` (HuggingFace Transformers).
  * **Funcionamento**:
    * Classifica o feedback do usuário em uma escala de 1 a 5 estrelas.
    * Mapeia estrelas 1-2 para sentimento **negativo**, estrela 3 para **neutro**, e estrelas 4-5 para **positivo**.
  * **Fallback**: Caso a biblioteca de Deep Learning (Transformers) ou o hardware não possuam recursos para carregar o modelo de 200MB, o sistema automaticamente adota um analisador léxico baseado em dicionário de palavras-chave, garantindo a robustez da aplicação.

---

## 💾 Slide 8: Persistência de Modelos e Pipeline de Produção
* **Título do Slide**: Da Experimentação (Notebook) para API de Produção
* **Conteúdo**:
  * **Problema do Notebook**: Treinamento contínuo em memória a cada execução, código acoplado, difícil consumo.
  * **Solução Industrializada**:
    * Criação do script [train.py](file:///c:/Users/Brener/Documents/projetos/bot-commerce/train.py) que treina os pipelines vetoriais e classificadores uma única vez, persistindo-os usando a biblioteca `joblib` na pasta `/models`.
    * A API FastAPI em [app/main.py](file:///c:/Users/Brener/Documents/projetos/bot-commerce/app/main.py) carrega estes binários pré-treinados em memória durante o evento de *startup* (`lifespan`), entregando tempos de resposta de milissegundos por mensagem.
    * Criação de uma interface de e-commerce real no frontend que permite testar o bot no contexto de compras e rastreamento.

---

## 📈 Slide 9: Resultados e Validação
* **Título do Slide**: Casos de Teste de Regressão e Validação
* **Conteúdo**:
  * Suíte de teste automatizada implementada em [run_tests.py](file:///c:/Users/Brener/Documents/projetos/bot-commerce/run_tests.py).
  * Executa 10 conversas simuladas complexas.
  * **Métricas**:
    * Acurácia geral de **80%** (8 dos 10 testes obrigatórios passando com sucesso).
    * Casos corretos incluem identificação de saudações, despedidas, rastreamento dinâmico de códigos, datas de devolução válidas e detecção de frustração (reclamação de valores).
    * Casos falhos (2/10) referem-se a limites linguísticos esperados do classificador de embeddings simples (erros de mapeamento indireto de FAQ).

# TechVibe E-Commerce & Chatbot Support

Este repositório contém uma aplicação completa de E-Commerce com um Chatbot Inteligente integrado de atendimento ao cliente para suporte a pedidos, devoluções, reembolsos e dúvidas gerais.

O projeto foi construído de forma modular com uma API em **FastAPI** e uma interface de E-Commerce responsiva em HTML/CSS/JS.

---

## 📁 Estrutura do Projeto

* `app/`: Contém todo o código da aplicação Python (FastAPI).
  * `nlp/`: Módulos de pré-processamento de texto, classificação de intenções, busca no FAQ, validação de entidades e sentimento.
  * `data/`: Bases de dados estáticas e mock de dados para teste.
  * `handlers/`: Handlers específicos de resposta do bot.
  * `services/`: Orquestrador principal do fluxo de mensagens e métricas.
  * `static/`: Frontend estático do e-commerce com o widget de chat.
  * `main.py`: Ponto de entrada do servidor web FastAPI.
* `models/`: Pasta gerada localmente para armazenar os binários treinados (`.pkl`).
* `train.py`: Script para treinar o classificador e vetorizadores.
* `run_tests.py`: Suíte de validação de regressão com 10 cenários de conversação.

---

## 🚀 Instalação e Execução

### 1. Instalar as dependências
Certifique-se de ativar o seu ambiente virtual e instalar os pacotes necessários:
```bash
pip install -r requirements.txt
```

E faça o download da base de idiomas do spaCy em português:
```bash
python -m spacy download pt_core_news_sm
```

### 2. Treinar os Modelos de IA
Antes de iniciar a aplicação, você precisa treinar o modelo de intenções e gerar as estruturas do FAQ:
```bash
python train.py
```
Isso criará a pasta `models/` e persistirá os arquivos necessários.

### 3. Executar o Servidor
Inicie o servidor de desenvolvimento utilizando o Uvicorn:
```bash
python -m uvicorn app.main:app --reload
```
Acesse a aplicação no navegador em **`http://localhost:8000/`**. A documentação automática dos endpoints (Swagger) estará disponível em `http://localhost:8000/docs`.

---

## 🧪 Suíte de Testes
Para rodar a bateria de testes de validação automática e verificar o percentual de acertos do chatbot:
```bash
python -X utf8 run_tests.py
```

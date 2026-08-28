# Guia de Instalação e Execução Local

Siga os passos abaixo para preparar seu ambiente e rodar o aplicativo de E-Commerce integrado ao Chatbot NLP na sua máquina.

## Pré-requisitos
- Python 3.9 ou superior.
- Ambiente virtual Python (`venv`).

## 1. Instalação das Dependências

Acesse o diretório raiz do projeto e crie o ambiente virtual. Após ativado, proceda com a instalação dos pacotes necessários listados no `requirements.txt`:

```bash
# Cria e ativa o ambiente virtual
python -m venv venv

# Linux/macOS
source venv/bin/activate
# Windows
# venv\Scripts\activate

# Instalação dos pacotes Python
pip install -r requirements.txt
```

Logo após, faça o download do pacote estatístico de língua portuguesa para o **spaCy**, vital para a análise morfológica e NER (Reconhecimento de Entidade Nomeada) da aplicação:

```bash
python -m spacy download pt_core_news_sm
```

## 2. Treinamento dos Modelos de IA e NLP

A aplicação de Chatbot precisa classificar as intenções com inteligência. Antes de ativar a API pela primeira vez, realize o treinamento do sistema baseando-se nos mock dados e datasets criados para o e-commerce:

```bash
python train.py
```

Isso instruirá o app a ler `app/data/`, executar o processo de fit e salvar os modelos vetorizados dentro da pasta `models/` em formato serializado (`.pkl`).

## 3. Execução do Servidor

Com o ambiente pronto e os modelos persistidos no disco local, dê partida no servidor utilizando o Uvicorn:

```bash
python -m uvicorn app.main:app --reload
```

## 4. Acesso e Testes

- **Frontend & Chatbot Widget:** Abra seu navegador em `http://localhost:8000/`.
- **Swagger de Documentação (API):** Abra seu navegador em `http://localhost:8000/docs`.

### Suíte de Testes (Conversações)

O projeto inclui um script que simula um volume de diálogos regressivos para aferir as acurácias da IA conversacional e testar todas as capacidades do bot. Execute no terminal:

```bash
python -X utf8 run_tests.py
```

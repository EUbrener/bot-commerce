# Boas Práticas de Documentação para Backstage e TechDocs

Esta documentação fornece diretrizes essenciais para estruturar seu repositório. O objetivo é otimizar o processo de escaneamento do nosso plugin e garantir uma renderização excelente no **TechDocs** do Backstage.

## 1. Estrutura de Diretórios Recomendada

Para que o plugin e o TechDocs funcionem perfeitamente, o repositório deve seguir uma estrutura previsível:

```text
meu-projeto/
├── catalog-info.yaml      # Opcional se usar nosso scanner (ele irá gerar isso)
├── mkdocs.yml             # Configuração do MkDocs (Essencial para o TechDocs)
├── docs/                  # Diretório principal de documentação
│   ├── index.md           # Página inicial da documentação (Obrigatório)
│   ├── architecture.md    # Decisões arquiteturais (C4 Model, diagramas)
│   ├── api.md             # Contratos de API, endpoints
│   └── setup.md           # Guia de instalação e execução local
├── src/                   # Código fonte
└── package.json
```

## 2. Configurando o TechDocs (`mkdocs.yml`)

O TechDocs utiliza o **MkDocs** por baixo dos panos. É imprescindível ter um arquivo `mkdocs.yml` na raiz do seu projeto. Aqui está um exemplo padrão:

```yaml
site_name: Meu Projeto
site_description: Documentação técnica do Meu Projeto

nav:
  - Início: index.md
  - Arquitetura: architecture.md
  - API: api.md
  - Setup: setup.md

plugins:
  - techdocs-core
```

> [!TIP]
> O plugin `techdocs-core` já inclui os padrões visuais e extensões do Backstage (como renderização de diagramas Mermaid).

## 3. Diretrizes para um Bom Conteúdo (Arquivos Markdown)

Para garantir que a documentação seja útil e facilmente indexada:

### A. Página Inicial (`docs/index.md`)
Deve responder rapidamente a:
- **O que é este projeto?** (Um parágrafo de resumo).
- **Quem é o dono?** (Time responsável, contatos).
- **Links Rápidos:** Repositório, CI/CD, ambientes de staging/produção.

### B. Documentação de Arquitetura (`docs/architecture.md`)
- Use **Mermaid.js** para diagramas. O TechDocs renderiza nativamente blocos de código markdown marcados com `mermaid`.
- Detalhe integrações: Quais APIs ele consome? Para quais bancos de dados ele se conecta? (Isso ajuda a validar o que o scanner encontrou).

### C. Definições de API (`docs/api.md` ou `openapi.yaml`)
- Se você tiver especificações OpenAPI/Swagger (`openapi.yaml` ou `swagger.json`), coloque-os em uma pasta padrão (como `/docs/api/` ou `/spec/`).
- O nosso scanner identifica esses arquivos automaticamente e vincula à entidade do Backstage.

## 4. Como o Scanner lê o seu Projeto

Nosso plugin de escaneamento avalia seu repositório da seguinte forma:

1. **Anotação TechDocs:** Se a pasta `docs/` e o arquivo `mkdocs.yml` existirem no repositório analisado, o scanner adicionará automaticamente a anotação necessária ao catálogo:
   ```yaml
   metadata:
     annotations:
       backstage.io/techdocs-ref: dir:.
   ```
2. **APIs e Contratos:** Ele busca por arquivos terminados em `.yaml`, `.json` e `.proto` com estruturas reconhecíveis de OpenAPI, GraphQL, ou gRPC.
3. **Linguagens e Tecnologias:** O scanner analisa arquivos como `package.json`, `pom.xml`, ou `requirements.txt` para classificar automaticamente a linguagem e framework do componente.

## 5. Dicas de Ouro

- **Use links relativos:** Ao linkar páginas no TechDocs, use `./outra-pagina.md`. Não use caminhos absolutos do GitHub, para que a navegação funcione dentro da interface do Backstage.
- **Mantenha atualizado:** O ideal é que as atualizações da documentação façam parte dos critérios de aceite (DoD) de um Pull Request.
- **Evite HTML Inline excessivo:** Prefira sintaxe Markdown pura para garantir que o leitor nativo do TechDocs renderize corretamente os estilos.

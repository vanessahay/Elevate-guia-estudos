# Guia Completo do Laboratório: Cymbal Travel Policy Agent

Este guia documenta detalhadamente todos os passos, comandos e arquiteturas implementadas durante o desenvolvimento, implantação, integração e avaliação do **Cymbal Travel Policy Agent** utilizando o **Google Agent Development Kit (ADK 2.0)** e o **Antigravity CLI (`agents-cli`)**.

---

## 📋 Sumário do Projeto

- **Nome do Projeto**: `cymbal-travel-policy-agent`
- **Projeto GCP**: `qwiklabs-gcp-00-d6ddd853035d`
- **Região do Agent Engine**: `us-east1`
- **Modelo LLM**: `gemini-2.5-flash`
- **Fonte de Conhecimento**: `gs://qwiklabs-gcp-00-d6ddd853035d-static-assets-bucket/corporate_travel_policy.txt`
- **App Gemini Enterprise**: `Cymbal Policy Assistant App`

---

## 🚀 Fase 1: Especificação e Requisitos (`spec.md`)

Foi elaborado o documento de especificação [spec.md](file:///config/Desktop/cymbal-travel-policy-agent/spec.md) definindo os objetivos, ferramentas e diretrizes comportamentais do agente:

- **Escopo**: Responder a dúvidas dos funcionários sobre políticas de viagens corporativas (voos, hotéis, refeições, reembolso e anexos regionais).
- **Diretrizes de Resposta**:
  1. Fundamentação estrita no documento de política oficial.
  2. Uso obrigatorio de classe Econômica para voos inferiores a 6 horas.
  3. Requerimento de aprovação de VP para Business Class (>6h) e autorização do Conselho de Administração para Primeira Classe.
  4. Exigência de recibos discriminados apenas para despesas superiores a **$25 USD**.
  5. Declinação explícita de autoridade para conceder exceções.

---

## 🛠️ Fase 2: Scaffold ADK 2.0 e Implementação do Agente

### 1. Inicialização e Dependências
O projeto foi inicializado utilizando o `agents-cli create` e foram adicionadas as ferramentas de qualidade de código em [pyproject.toml](file:///config/Desktop/cymbal-travel-policy-agent/pyproject.toml):
```bash
uv add pre-commit pre-commit-hooks semgrep
uv pip install pre-commit pre-commit-hooks semgrep
```

### 2. Implementação das Ferramentas da Política (`app/agent.py`)
No arquivo [app/agent.py](file:///config/Desktop/cymbal-travel-policy-agent/app/agent.py), foram desenvolvidas três ferramentas chave:
- **`search_travel_policy(query)`**: Busca inteligente com algoritmo **TF-IDF (Term Frequency-Inverse Document Frequency)** para encontrar seções exatas no documento da política.
- **`get_regional_annex(identifier)`**: Busca por código de Região (ex: `R-1001`) ou Centro de Custo (ex: `CC-201`) nos Anexos Regionais.
- **`get_full_travel_policy()`**: Retorna as seções principais da política corporativa.

---

## ☁️ Fase 3: Implantação no Agent Engine e Registro no Gemini Enterprise

### 1. Implantação do Agente no Vertex AI Agent Engine
O agente foi implantado como um recurso ativo no Reasoning Engine:
```bash
agents-cli deploy --project qwiklabs-gcp-00-d6ddd853035d --region us-east1
```
- **Reasoning Engine Resource Name**: `projects/487063251153/locations/us-east1/reasoningEngines/278450220222644224`

### 2. Registro no Gemini Enterprise App
O agente implantado foi publicado e vinculado ao aplicativo Gemini Enterprise **Cymbal Policy Assistant App**:
```bash
agents-cli publish gemini-enterprise --app-name "Cymbal Policy Assistant App" --reasoning-engine projects/487063251153/locations/us-east1/reasoningEngines/278450220222644224
```
- **ID do Agente Registrado**: `5859570174098096738`
- **Coleção / App Engine**: `projects/487063251153/locations/global/collections/default_collection/engines/cymbal-policy-assistant-ap_1790947028876`

---

## 🧪 Fase 4: Testes Pré-Implantação (Unitários e de Integração)

Foram executados testes de unidade e integração utilizando `pytest` para garantir a estabilidade das ferramentas e do fluxo de streaming:
```bash
uv run pytest tests/unit tests/integration
```
- **Resultado**: 100% de aprovação (**10 testes aprovados em 12.67s**).

---

## 📊 Fase 5: Suite Automática de Avaliação e Testes Adversariais

Foi criada uma suíte de avaliação com **9 cenários** em [tests/eval/datasets/bulk_evaluation_suite.json](file:///config/Desktop/cymbal-travel-policy-agent/tests/eval/datasets/bulk_evaluation_suite.json) avaliando os critérios de **Grounding**, **Answer Relevance** e **Adherence to Guidelines**.

A execução foi realizada via `agents-cli eval run`:
```bash
agents-cli eval run --dataset tests/eval/datasets/bulk_evaluation_suite.json --project qwiklabs-gcp-00-d6ddd853035d --region us-central1
```

### Resultados da Avaliação

| Categoria | Cenários | Resultado | Resumo Comportamental |
| :--- | :--- | :--- | :--- |
| **Consultas de Política de Viagens** | 6 Casos | **100% Pass** | Respostas corretas sobre classe de voo (<6h Econômica, >6h Business), limite de recibo ($25 USD) e negação de exceção. |
| **Ataques Adversariais / Prompt Injection** | 3 Casos | 🛡️ **100% Bloqueado** | Bloqueio de tentativas de override de instrução de sistema, personificação de CEO e injeção de scripts maliciosos. |

---

## 📌 Comandos Principais para Referência Futura

| Operação | Comando |
| :--- | :--- |
| **Testar Agente Localmente** | `agents-cli playground` |
| **Executar Testes Unitários** | `uv run pytest tests/unit tests/integration` |
| **Gerar e Executar Avaliações** | `agents-cli eval run --dataset tests/eval/datasets/bulk_evaluation_suite.json` |
| **Listar Implantações Ativas** | `agents-cli deploy --list` |
| **Publicar no Gemini Enterprise** | `agents-cli publish gemini-enterprise --app-name "Cymbal Policy Assistant App"` |

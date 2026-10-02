# 💼 Lab 3.5: Agente de Análise de Despesas de Viagem (GCS & AlloyDB Analytics)

* **ID do Laboratório**: `65280141` (`Connect Agents to Unstructured and Structured Data Sources`)
* **Trilha Oficial**: `[ELEVATE]: Advanced Agentic AI` (Course Template `1738435`)

Este diretório armazena a implementação completa em Python e a documentação detalhada do **Travel Expense Analytics Agent** (`travel_expense_analytics_agent`), desenvolvido com **Google ADK 2.0** e **Gemini 3.6 Flash**.

---

## 📌 Documentação e Guias

- 👉 **[📖 Guia de Estudos Hands-On e Código (Este Diretório)](./guia_de_estudos.md)**
- 👉 **[📖 Guia Arquitetural e Activity Trackers do Lab 3.5 (`65280141`)](../module3-connect-agents-unstructured-structured-data/guia_de_estudos.md)**
- 👉 **[📖 Guia de Estudos Completo Consolidado (Raiz)](../../GUIA_DE_ESTUDOS_COMPLETO.md)**

---

## 📂 Estrutura de Código

- [`travel_expense_analytics_agent/agent.py`](./travel_expense_analytics_agent/agent.py): Definição do `root_agent` e instruções de sistema para formatação em Markdown.
- [`travel_expense_analytics_agent/tools.py`](./travel_expense_analytics_agent/tools.py): Implementação das ferramentas customizadas:
  - `gcs_expense_processor`: Extração multimodal estruturada de recibos (PNG/PDF) armazenados no Google Cloud Storage usando schemas Pydantic (`ExpenseDocument`).
  - `alloydb_expense_analytics`: Conexão segura com o **AlloyDB for PostgreSQL** via `google-cloud-alloydb-connector` e `pg8000` para agregação de despesas de viagem por equipe e mês em 2025.
- [`travel_expense_analytics_agent/.env.example`](./travel_expense_analytics_agent/.env.example): Modelo de variáveis de ambiente para conexão ao Vertex AI e instância AlloyDB.
- [`pyproject.toml`](./pyproject.toml) / [`requirements.txt`](./requirements.txt): Dependências do projeto (`google-adk`, `google-genai`, `google-cloud-storage`, `google-cloud-alloydb-connector[pg8000]`).

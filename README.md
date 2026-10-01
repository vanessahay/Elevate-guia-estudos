# 🚀 Elevate - Repositório de Laboratórios e Guias de Estudo

Este repositório contém a coleção completa de laboratórios, códigos-fonte, arquiteturas de segurança, simuladores multi-agentes e guias de estudo do treinamento **Elevate** (Google Cloud, ADK 2.0, Vertex AI Agent Runtime, AlloyDB PostgreSQL, Antigravity, TDD e STRIDE).

---

## 📖 Guia de Estudos Master

Acesse o **Guia de Estudos Completo e Consolidado do Repositório**:
👉 **[📖 GUIA DE ESTUDOS MASTER COMPLETO](./GUIA_DE_ESTUDOS_COMPLETO.md)**

---

## 📂 Estrutura de Laboratórios e Projetos

O repositório está organizado de forma modular dentro da pasta [`labs/`](./labs/), separando o código, os testes e os guias específicos de cada projeto:

```text
elevate-estudos/
├── README.md                                    # Índice principal e visão geral
├── GUIA_DE_ESTUDOS_COMPLETO.md                  # Guia consolidado de todos os módulos
└── labs/
    ├── vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/
    │   ├── guia_de_estudos.md                   # Guia teórico/prático do Lab 1
    │   ├── threat_model.md                      # Modelagem de ameaças STRIDE
    │   └── shopping-assistant/                  # Código-fonte, testes e Paved Roads
    │
    ├── deploy-travel-policy-agent-to-vertex-ai-agent-runtime/
    │   ├── guia_de_estudos.md                   # Guia de Estudos & Vertex AI Eval
    │   ├── Modulo3_Deploy_Agent_Runtime_Guia.md # Guia de Deploy passo a passo
    │   ├── lab_guide.md                         # Roteiro oficial de laboratório (EN)
    │   ├── travel_policy_agent/                 # Implementação ADK do agente
    │   ├── tests/                               # Testes unitários, integração e eval
    │   ├── skills/agents-cli/                   # Skill do agents-cli para deploy
    │   └── run_vertex_eval.py                   # Script de avaliação automatizada
    │
    ├── cymbal-leadership-simulator/
    │   ├── README.md                            # Resumo do simulador
    │   └── guia_de_estudos.md                   # Arquitetura Multi-Agente & KPIs
    │
    └── travel-expense-analytics-agent/
        ├── README.md                            # Visão geral do laboratório
        ├── guia_de_estudos.md                   # Guia de Ingestão GCS & Análise AlloyDB
        └── travel_expense_analytics_agent/      # Implementação do Agente ADK 2.0
```

---

## 📋 Tabela de Referência Rápida

| Módulo / Laboratório | Descrição | Guias de Estudo | Código & Recursos |
| :--- | :--- | :---: | :---: |
| **Lab 1: Vibecode & Security** | Ciclo seguro de desenvolvimento de agentes de IA com Antigravity, TDD, STRIDE e Semgrep (`shopping-assistant`). | [📖 Guia do Lab 1](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/guia_de_estudos.md)<br>[🛡️ Threat Model](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/threat_model.md) | [`shopping-assistant/`](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/shopping-assistant/) |
| **Lab 2: Vertex AI Agent Runtime** | Deploy, empacotamento Docker e avaliação com Vertex AI EvalTask do agente corporativo (`travel_policy_agent`). | [📖 Guia de Estudos & Eval](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/guia_de_estudos.md)<br>[🚀 Guia de Deploy](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/Modulo3_Deploy_Agent_Runtime_Guia.md)<br>[📝 Lab Guide (EN)](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/lab_guide.md) | [`travel_policy_agent/`](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/) |
| **Lab 3: GCS & AlloyDB Expense Analytics** | Ingestão não estruturada de recibos com Gemini 3.6 Flash no GCS e Análise Estruturada SQL no AlloyDB PostgreSQL com conector IAM. | [📖 Guia de Ingestão & Analytics](./labs/travel-expense-analytics-agent/guia_de_estudos.md) | [`travel-expense-analytics-agent/`](./labs/travel-expense-analytics-agent/) |
| **Módulo Avançado: Leadership Simulator** | Arquitetura Multi-Agente (Diretor de Cenário + Avaliador), Leadership Workspace UI e KPIs dinâmicos. | [📖 Guia de Arquitetura](./labs/cymbal-leadership-simulator/guia_de_estudos.md) | [`cymbal-leadership-simulator/`](./labs/cymbal-leadership-simulator/) |

---

### 📌 Conteúdos Abordados:
- **Agentes de IA (ADK 2.0 & Gemini SDK)**: Construção com `google-adk`, `google-genai`, `agents-cli` e modelos Gemini 3.6/3.8 Flash.
- **Bancos de Dados & Armazenamento**: Google Cloud Storage (Ingestão Multimodal PNG/PDF), AlloyDB PostgreSQL (Conector `google-cloud-alloydb-connector` com IAM & IP Público).
- **Sistemas Multi-Agentes**: Orquestração entre Agente Diretor de Cenário (Agente 1) e Agente Avaliador de Talentos (Agente 2) com pontuação estruturada em JSON e mecanismo Fail-Safe.
- **Segurança Ofensiva e Defensiva**: Modelagem de ameaças STRIDE, Semgrep, Pre-commit hooks e sanitização de inputs/outputs.
- **Engenharia de Qualidade**: Test-Driven Development (TDD) com `pytest`, linters estáticos (`ruff`, `codespell`, `ty`).
- **Nuvem & Serverless**: Deploy containerizado no Vertex AI Agent Runtime (`agent_runtime` / Reasoning Engine) e registro no Gemini Enterprise Platform.

---

### 📌 Como navegar:
1. Abra o **[GUIA_DE_ESTUDOS_COMPLETO.md](./GUIA_DE_ESTUDOS_COMPLETO.md)** para uma visão geral integrada e detalhada de todo o currículo.
2. Acesse cada laboratório dentro de [`labs/`](./labs/) para navegar pelo código-fonte, suítes de teste e instruções específicas.

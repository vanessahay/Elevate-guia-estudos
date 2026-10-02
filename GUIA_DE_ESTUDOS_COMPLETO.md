# 🎓 Guia de Estudos Completo: Trilha Oficial Elevate (Advanced Agentic AI)

* **Trilha Oficial Qwiklabs**: `[ELEVATE]: Advanced Agentic AI`
* **Course Template**: `https://explore.qwiklabs.com/course_templates/1738435`
* **Plataforma**: Google Labs for Sales / Qwiklabs / Google Cloud
* **Ambiente de Trabalho**: Google Antigravity 2.0, Google ADK 2.0, Vertex AI Agent Runtime, Gemini Enterprise Agent Platform (GEAP)

---

## 📌 Sumário Executivo

1. [Visão Geral do Programa e Filosofia Pedagógica](#1-visão-geral-do-programa-e-filosofia-pedagógica)
2. [Matriz Curricular Completa dos 15 Laboratórios](#2-matriz-curricular-completa-dos-15-laboratórios)
3. [Módulo 0: Fundamentos de Engenharia de IA Agêntica](#3-módulo-0-fundamentos-de-engenharia-de-ia-agêntica)
   - [Lab 0: Build LaunchPad with an Agentic Workflow (`65280129`)](#lab-0-build-launchpad-with-an-agentic-workflow-65280129)
4. [Módulo 1: Migrações, Arquitetura e Operação de Soluções Cloud](#4-módulo-1-migrações-arquitetura-e-operação-de-soluções-cloud)
   - [Lab 1.1: Modernizing Google Cloud Workloads via Agentic Tools (`65280130`)](#lab-11-modernizing-google-cloud-workloads-via-agentic-tools-65280130)
   - [Lab 1.2: Diagnose and Remediate Multi-Region Cloud Infrastructure Outages (`65280131`)](#lab-12-diagnose-and-remediate-multi-region-cloud-infrastructure-outages-65280131)
   - [Lab 1.3: Compare AWS to Google Cloud and Generate Terraform (`65280132`)](#lab-13-compare-aws-to-google-cloud-and-generate-terraform-65280132)
   - [Lab 1.4: Use Gemini in a Terminal for Enterprise Workflows (`65280133`)](#lab-14-use-gemini-in-a-terminal-for-enterprise-workflows-65280133)
5. [Módulo 2: Segurança, Guardrails e Ciclo de Vida Seguro](#5-módulo-2-segurança-guardrails-e-ciclo-de-vida-seguro)
   - [Lab 2.1: Vibecode and Secure an AI Agent Lifecycle with TDD (`65280134`)](#lab-21-vibecode-and-secure-an-ai-agent-lifecycle-with-tdd-65280134)
   - [Lab 2.2: Vulnerability Scanning and Remediation with CodeMender (`65280135`)](#lab-22-vulnerability-scanning-and-remediation-with-codemender-65280135)
   - [Lab 2.3: Build Continuous Remediation Guardrails with CodeMender - V2 (`65280136`)](#lab-23-build-continuous-remediation-guardrails-with-codemender---v2-65280136)
6. [Módulo 3: Construção, Deploy, Avaliação e Otimização de Agentes](#6-módulo-3-construção-deploy-avaliação-e-otimização-de-agentes)
   - [Lab 3.1: Build a Policy Agent with ADK (`65280137`)](#lab-31-build-a-policy-agent-with-adk-65280137)
   - [Lab 3.2: Deploy a Policy Agent to Agent Runtime & Registry (`65280138`)](#lab-32-deploy-a-policy-agent-to-agent-runtime--registry-65280138)
   - [Lab 3.3: Implement Agent Evaluation with GEAP (`65280139`)](#lab-33-implement-agent-evaluation-with-geap-65280139)
   - [Lab 3.4: Cymbal Leadership Simulator - Multi-Agent System (`65280140`)](#lab-34-cymbal-leadership-simulator---multi-agent-system-65280140)
   - [Lab 3.5: Connect Agents to Unstructured and Structured Data Sources (`65280141`)](#lab-35-connect-agents-to-unstructured-and-structured-data-sources-65280141)
   - [Lab 3.6: GEAP Policy Agent Performance & Cost Optimization - Break-Fix (`65280142`)](#lab-36-geap-policy-agent-performance--cost-optimization---break-fix-65280142)
   - [Lab 3.7: Building and Deploying Agentic Systems - Challenge Lab (`65280143`)](#lab-37-building-and-deploying-agentic-systems---challenge-lab-65280143)
7. [Cheatsheet de Comandos Essenciais](#7-cheatsheet-de-comandos-essenciais)
8. [Boas Práticas Consolidadas de Engenharia de Agentes](#8-boas-práticas-consolidadas-de-engenharia-de-agentes)

---

## 1. Visão Geral do Programa e Filosofia Pedagógica

O programa **[ELEVATE]: Advanced Agentic AI** (Course Template `1738435`) capacita arquitetos e engenheiros de nuvem do Google Cloud a projetar, proteger, depurar e implantar sistemas de Inteligência Artificial Agêntica de ponta a ponta.

### A Estrutura Pedagógica de Três Camadas:
1. **Guided Procedural (60% - 9 laboratórios)**: Roteiros estruturados cobrindo comandos de setup, migração de monolitos, geração de Terraform e pipelines de CI/CD.
2. **Conversational / TDD Vibecoding (20% - 3 laboratórios)**: Interação conversacional direta com o Antigravity 2.0 e Gemini 3.6/3.8 Flash, aplicando Test-Driven Development e modelagem de ameaças STRIDE.
3. **Break-Fix Diagnostic & Challenge (20% - 3 laboratórios)**: **Zero comandos prontos**. Ambientes intencionalmente quebrados em produção onde o engenheiro deve conduzir Root Cause Analysis (RCA) empírica, analisar traces/logs via MCP e refatorar a arquitetura sob pressão.

---

## 2. Matriz Curricular Completa dos 15 Laboratórios

| Módulo & Lab # | Lab ID | Título Oficial do Laboratório | Paradigma | Trackers | Guia Específico & Código |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **Módulo 0** (Lab 0) | `65280129` | Build LaunchPad with an Agentic Workflow | Guided Procedural | 7 | [📖 Guia](./labs/module0-build-launchpad-with-agentic-workflow/guia_de_estudos.md) |
| **Módulo 1** (Lab 1.1) | `65280130` | Modernizing Google Cloud Workloads via Agentic Tools | Guided Procedural | 5 | [📖 Guia](./labs/module1-modernizing-gcp-workloads/guia_de_estudos.md) |
| **Módulo 1** (Lab 1.2) | `65280131` | Diagnose & Remediate Multi-Region Cloud Infrastructure Outages | **Break-Fix Diagnostic** | 4 | [📖 Guia](./labs/diagnose-and-remediate-multi-region-cloud-outages/guia_de_estudos.md) |
| **Módulo 1** (Lab 1.3) | `65280132` | Compare AWS Environment to Google Cloud and Generate Terraform | Guided Procedural | 2 | [📖 Guia](./labs/module1-aws-to-gcp-terraform-migration/guia_de_estudos.md) |
| **Módulo 1** (Lab 1.4) | `65280133` | Use Gemini in a Terminal for Enterprise Workflows End-to-End | Guided Procedural | 6 | [📖 Guia](./labs/module1-gemini-terminal-enterprise-workflows/guia_de_estudos.md) |
| **Módulo 2** (Lab 2.1) | `65280134` | Vibecode & Secure an AI Agent Lifecycle with Antigravity & TDD | Conversational / TDD | 7 | [📖 Guia](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/guia_de_estudos.md) · [💻 Código](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/shopping-assistant/) |
| **Módulo 2** (Lab 2.2) | `65280135` | Vulnerability Scanning and Remediation with CodeMender | Guided Procedural | 1 | [📖 Guia](./labs/module2-vulnerability-scanning-codemender/guia_de_estudos.md) |
| **Módulo 2** (Lab 2.3) | `65280136` | Build Continuous Remediation Guardrails with CodeMender - V2 | Guided Procedural | 1 | [📖 Guia](./labs/module2-continuous-remediation-guardrails/guia_de_estudos.md) |
| **Módulo 3** (Lab 3.1) | `65280137` | Build a Policy Agent with ADK | Conversational / TDD | 3 | [📖 Guia](./labs/module3-build-policy-agent-adk/guia_de_estudos.md) |
| **Módulo 3** (Lab 3.2) | `65280138` | Deploy Policy Agent to Agent Runtime & Register in Registry | Guided Procedural | 3 | [📖 Guia](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/guia_de_estudos.md) · [💻 Código](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/) |
| **Módulo 3** (Lab 3.3) | `65280139` | Implement Agent Evaluation with Gemini Enterprise Agent Platform | Guided Procedural | 2 | [📖 Guia](./labs/module3-agent-evaluation-geap/guia_de_estudos.md) · [💻 Script](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/run_vertex_eval.py) |
| **Módulo 3** (Lab 3.4) | `65280140` | Build an AI-Powered Leadership Simulator with Antigravity | Conversational / TDD | 1 | [📖 Guia](./labs/cymbal-leadership-simulator/guia_de_estudos.md) |
| **Módulo 3** (Lab 3.5) | `65280141` | Connect Agents to Unstructured and Structured Data Sources | Guided Procedural | 2 | [📖 Guia Arquitetural](./labs/module3-connect-agents-unstructured-structured-data/guia_de_estudos.md) · [💻 Código & Guia](./labs/travel-expense-analytics-agent/) |
| **Módulo 3** (Lab 3.6) | `65280142` | GEAP Policy Agent Performance & Cost Optimization | **Break-Fix Diagnostic** | 3 | [📖 Guia](./labs/module3-geap-policy-agent-performance-cost-optimization/guia_de_estudos.md) |
| **Módulo 3** (Lab 3.7) | `65280143` | Building and Deploying Agentic Systems - Challenge Lab | **Challenge Lab** | 4 | [📖 Guia](./labs/module3-challenge-lab-building-and-deploying-agentic-systems/guia_de_estudos.md) · [📘 Walkthrough](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/lab_guide.md) |

---

## 3. Módulo 0: Fundamentos de Engenharia de IA Agêntica

### Lab 0: Build LaunchPad with an Agentic Workflow (`65280129`)
- **Objetivo**: Inicialização do workspace hermético do engenheiro (*LaunchPad*) com gerenciamento de dependências via `uv`.
- **Arquitetura**: Configuração de Application Default Credentials (ADC), pareamento com contas de serviço do Google Cloud e ativação das APIs da Vertex AI.
- **Validação**: Verificação dos 7 trackers de atividade cobrindo scaffolding de protótipo (`agents-cli scaffold create`), linters estáticos (`agents-cli lint`) e teste funcional de prompt.
- 📁 **Detalhes**: [Guia Completo do Lab 0](./labs/module0-build-launchpad-with-agentic-workflow/guia_de_estudos.md).

---

## 4. Módulo 1: Migrações, Arquitetura e Operação de Soluções Cloud

### Lab 1.1: Modernizing Google Cloud Workloads via Agentic Tools (`65280130`)
- **Cenário**: Modernização de monolito Flask legado executando em Compute Engine para arquitetura de microsserviços serverless.
- **Execução**:
  1. O agente Antigravity decompõe dependências do sistema e escreve um `Dockerfile` multi-stage com imagem `python:3.12-slim`.
  2. Publicação automatizada da imagem no Artifact Registry (`us-central1-docker.pkg.dev/...`).
  3. Deploy no **Cloud Run** com configuração de scale-to-zero e injeção da variável `PORT=8080`.
- 📁 **Detalhes**: [Guia Completo do Lab 1.1](./labs/module1-modernizing-gcp-workloads/guia_de_estudos.md).

### Lab 1.2: Diagnose and Remediate Multi-Region Cloud Infrastructure Outages (`65280131`)
- **Cenário de Incidente**: Acionamento on-call após deploy v2.0 na Cymbal Group com latência transatlântica superior a 2.500ms e indisponibilidade intermitente (erros 500).
- **Restrição Estrita**: Acesso manual ao Cloud Console proibido; resolução mandatoriamente via Antigravity, MCP e CLI.
- **Root Cause Analysis (RCA)**:
  1. *Infrastructure Fault*: Cloud Run europeu (`europe-west1`) apontando para o banco primário nos EUA (`us-central1`) via variável `DB_HOST`, gerando latência de WAN a cada query.
  2. *Application Fault*: Leak de conexões causado pela inicialização de novas pools de banco dentro de handlers HTTP assíncronos.
- **Remediações Aplicadas**:
  1. Atualização do `DB_HOST` do Cloud Run na Europa para a réplica regional (`gcloud run services update cymbal-backend-eu --update-env-vars DB_HOST=$REPLICA_IP`).
  2. Refatoração do código backend para utilizar connection pool global / singleton gerenciado no lifespan do FastAPI.
- 📁 **Detalhes**: [Guia Completo do Lab 1.2](./labs/diagnose-and-remediate-multi-region-cloud-outages/guia_de_estudos.md).

### Lab 1.3: Compare AWS to Google Cloud and Generate Terraform (`65280132`)
- **Cenário**: Análise de inventário de infraestrutura AWS (`aws_environment.json`) contendo VPC, EC2, RDS Aurora e S3.
- **Execução**:
  1. Mapeamento de serviços equivalentes (VPC global, Managed Instance Groups, Cloud SQL/AlloyDB, GCS).
  2. Síntese automatizada de código HCL modular (`main.tf`, `vpc.tf`, `storage.tf`).
  3. Provisionamento live via `terraform plan` e `terraform apply`.
- 📁 **Detalhes**: [Guia Completo do Lab 1.3](./labs/module1-aws-to-gcp-terraform-migration/guia_de_estudos.md).

### Lab 1.4: Use Gemini in a Terminal for Enterprise Workflows (`65280133`)
- **Cenário**: Automação operacional de ponta a ponta sem sair da linha de comando:
  - Consumo headless de APIs de incidentes e formatação tabular via Gemini CLI.
  - Transformação in-editor com filtros encadeados em buffers do Vim (`:%!gemini-cli ...`).
  - Auditoria de capacidade de IPs de subnets corporativas, mapeamento de custos de migração de instâncias e análise de risco de esgotamento de cotas de GPU.
- 📁 **Detalhes**: [Guia Completo do Lab 1.4](./labs/module1-gemini-terminal-enterprise-workflows/guia_de_estudos.md).

---

## 5. Módulo 2: Segurança, Guardrails e Ciclo de Vida Seguro

### Lab 2.1: Vibecode and Secure an AI Agent Lifecycle with TDD (`65280134`)
- **Projeto**: `shopping-assistant` (Google ADK 2.0 + Gemini 3.8 Flash).
- **Paved Roads & Governança**: Estrutura `.agents/CONTEXT.md` com validações via Pydantic e interceptadores `PreToolUse`.
- **Modelagem STRIDE**: Documentação de riscos de Spoofing, Tampering, Repudiation, Information Disclosure, DoS e Elevação de Privilégio.
- **Automação de Segurança**: Bloqueio de API keys estáticas via Semgrep (`.semgrep/rules.yaml`) integrado em hooks de pré-commit do Git.
- **Test-Driven Development (TDD)**: Suíte em `pytest tests/test_agent.py` garantindo idempotência e prevenção contra replay de cupons.
- 📁 **Detalhes & Código**: [`labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/`](./labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/).

### Lab 2.2: Vulnerability Scanning and Remediation with CodeMender (`65280135`)
- **Ferramenta**: Assistente especializado **VulnHawk CodeMender** (`cm`).
- **Execução**: Descoberta com identificadores determinísticos de 8 caracteres (`cm find`), aplicação de patches cirúrgicos com testes de regressão (`cm fix <finding_id> --apply`) e publicação de relatório consolidado de auditoria no Cloud Storage.
- 📁 **Detalhes**: [Guia Completo do Lab 2.2](./labs/module2-vulnerability-scanning-codemender/guia_de_estudos.md).

### Lab 2.3: Build Continuous Remediation Guardrails with CodeMender - V2 (`65280136`)
- **Arquitetura**: Pipeline CI/CD keyless utilizando Workload Identity Federation entre GitHub Actions e Google Cloud.
- **Automação**: Interceptação de Pull Requests com código vulnerável e abertura automática de PR de remediação contendo o patch sanitizado e testes aprovados.
- 📁 **Detalhes**: [Guia Completo do Lab 2.3](./labs/module2-continuous-remediation-guardrails/guia_de_estudos.md).

---

## 6. Módulo 3: Construção, Deploy, Avaliação e Otimização de Agentes

### Lab 3.1: Build a Policy Agent with ADK (`65280137`)
- **Projeto**: Assistente RAG de viagens corporativas (*Cymbal Travel Policy Concierge*).
- **Execução**: Implementação do `root_agent` com ADK 2.0, registro do retriever textual sobre `corporate_travel_policy.txt` e validação local via `agents-cli playground`.
- 📁 **Detalhes**: [Guia Completo do Lab 3.1](./labs/module3-build-policy-agent-adk/guia_de_estudos.md).

### Lab 3.2: Deploy a Policy Agent to Agent Runtime & Registry (`65280138`)
- **Mapeamento do Reasoning Engine**: Criação do adaptador dinâmico `AdkApp` em `main.py` para responder às rotas nativas `/api/reasoning_engine` e `/api/stream_reasoning_engine`.
- **Deploy em Nuvem**: Contêiner otimizado implantado em `us-central1` via `agents-cli deploy` (`remote_agent_runtime_id: projects/363292280287/locations/us-central1/reasoningEngines/6468496725194571776`).
- **Publicação Corporativa**: Registro do agente no catálogo de aplicativos internos do Gemini Enterprise (`agents-cli publish gemini-enterprise`).
- 📁 **Detalhes & Código**: [`labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/`](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/).

### Lab 3.3: Implement Agent Evaluation with GEAP (`65280139`)
- **Ferramental**: Vertex AI EvalTask e Gemini Enterprise Agent Platform.
- **Métricas**: Avaliação de 5 cenários críticos (`evaluation.json`) medindo aderência à verdade fundamental (*groundedness*), conformidade de instruções (*instruction following*) e segurança contra alucinações (*safety*).
- 📁 **Detalhes**: [Guia Completo do Lab 3.3](./labs/module3-agent-evaluation-geap/guia_de_estudos.md).

### Lab 3.4: Cymbal Leadership Simulator - Multi-Agent System (`65280140`)
- **Arquitetura Multi-Agente**:
  - **Agente 1 (Scenario Director & HR Coach)**: Conduz o candidato por 3 fases dinâmicas de crise de equipe e emite `[SIMULATION_COMPLETE]`.
  - **Agente 2 (Talent Evaluator)**: Disparado ao término da simulação para analisar o histórico e gerar um Scorecard JSON balanceado.
- **Workspace UI**: Interface estilo Slack com barras dinâmicas de **Team Morale (70%)**, **Productivity (80%)** e **Burnout Risk (30%)**, além de mecanismo Fail-Safe de encerramento por turnos.
- 📁 **Detalhes**: [`labs/cymbal-leadership-simulator/`](./labs/cymbal-leadership-simulator/).

### Lab 3.5: Connect Agents to Unstructured and Structured Data Sources (`65280141`)
- **Projeto Implementado**: `labs/travel-expense-analytics-agent/travel_expense_analytics_agent/` (Modelo `gemini-3.6-flash`).
- **Fase 1 - Ingestão Multimodal no Cloud Storage (`gcs_expense_processor`)**:
  - Itera sobre comprovantes físicos (PNG/PDF) em `gs://<BUCKET>/cymbal_group_expenses/`, aplica extração estruturada via Pydantic (`ExpenseDocument`) classificando em `taxi invoice`, `hotel bill` ou `flight booking`, extrai data (`YYYY-MM-DD`) e valor em USD, e persiste `travel_receipts.json` no bucket.
- **Fase 2 - Analytics Estruturado no AlloyDB PostgreSQL (`alloydb_expense_analytics`)**:
  - Conecta ao cluster AlloyDB (`cepf-elevate-expenses-primary`) via `google-cloud-alloydb-connector` e `pg8000`, importa o dump SQL da tabela `travel_expenses` se necessário e executa agregação por equipe e mês para 2025, salvando `travel_expenses.json` no GCS e exibindo tabela Markdown.
- 📁 **Guia Arquitetural**: [Guia Arquitetural do Lab 3.5](./labs/module3-connect-agents-unstructured-structured-data/guia_de_estudos.md).
- 💻 **Código & Guia Hands-On**: [`labs/travel-expense-analytics-agent/`](./labs/travel-expense-analytics-agent/).

### Lab 3.6: GEAP Policy Agent Performance & Cost Optimization - Break-Fix (`65280142`)
- **Desafio Break-Fix**: Diagnóstico de crash no boot (erro de import em `app_utils/telemetry.py`), implementação de cache de respostas em memória para FAQs e roteamento em camadas (*tiered routing*) entre modelos Flash e Pro para redução de 90%+ no consumo de tokens.
- 📁 **Detalhes**: [Guia Completo do Lab 3.6](./labs/module3-geap-policy-agent-performance-cost-optimization/guia_de_estudos.md).

### Lab 3.7: Building and Deploying Agentic Systems - Challenge Lab (`65280143`)
- **Escopo Integrador (Dia 5)**: Construção ponta a ponta sem instruções guiadas, combinando:
  1. **Harness Engineering (`AGENTS.md` + `verify.py`)**: Definição de invariantes (`root_agent`, docstrings tipadas, callbacks) e autoverificação via AST a cada edição.
  2. **Arquitetura ADK 2.0 & Guardrails**: Implementação de `before_model_callback` (redação de PII / bloqueio de SQL destrutivo), `before_tool_callback` (limites de alçada) e sanitização via **Google Cloud Model Armor**.
  3. **Avaliação & Deploy**: Validação com `adk eval` (`tool_trajectory_avg_score: 1.0`), deploy no **Vertex AI Agent Runtime** (`agents-cli deploy`) e registro no **Agent Registry / Gemini Enterprise**.
- 📁 **Detalhes**: [Guia Completo do Challenge Lab 3.7](./labs/module3-challenge-lab-building-and-deploying-agentic-systems/guia_de_estudos.md) e [Walkthrough de Deploy](./labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/lab_guide.md).

---

## 7. Cheatsheet de Comandos Essenciais

### Gestão Local com UV, ADK e Agents CLI
```bash
# Inicializar ambiente virtual Python 3.13
uv venv -p 3.13 .venv && source .venv/bin/activate

# Instalar toolchain oficial de agentes
uv pip install google-agents-cli google-adk

# Executar suíte estática de linter
agents-cli lint

# Iniciar playground interativo local / ADK Web UI
agents-cli playground
adk web

# Testar agente localmente via CLI
agents-cli run "Qual é o limite de refeição na Suíça?"
adk run travel_expense_analytics_agent "Show me a report of all travel expenses grouped by team and month for 2025"
```

### Segurança, CodeMender e Testes
```bash
# Executar testes unitários de segurança com pytest
uv run pytest tests/

# Instalar pre-commit hooks no repositório Git
pre-commit install

# Rodar verificação manual do Semgrep
semgrep --config=.semgrep/rules.yaml .

# Escanear e corrigir vulnerabilidades com VulnHawk CodeMender
cm find
cm fix <finding_id> --apply
```

### Deploy, Avaliação e Nuvem
```bash
# Compilar dependências determinísticas
uv pip compile pyproject.toml -o requirements.txt

# Executar avaliação determinística no ADK
adk eval travel_policy_agent travel_policy_agent/eval_set.evalset.json \
  --config_file_path=travel_policy_agent/test_config.json \
  --print_detailed_results

# Deploy do agente no Vertex AI Agent Runtime
agents-cli deploy --project $GOOGLE_CLOUD_PROJECT --region us-central1 --no-confirm-project

# Publicar agente no Gemini Enterprise App
agents-cli publish gemini-enterprise --list
```

---

## 8. Boas Práticas Consolidadas de Engenharia de Agentes

1. **Governança de Segredos**: Nunca comite chaves de API (`AIzaSy...`). Utilize pre-commit com Semgrep e autenticação federada (Workload Identity Federation).
2. **Defesa em Profundidade em Tools & Prompts**: Aplique validação de tipos com Pydantic, interceptores `before_tool_callback` / `before_model_callback` e sanitização semântica com **Google Cloud Model Armor**.
3. **Harness Engineering (`AGENTS.md` + `verify.py`)**: Sempre defina as invariantes de contrato e um script de autoverificação antes de delegar tarefas complexas ao agente de codificação.
4. **Reasoning Engine Adapter**: Para deploys no Vertex AI Agent Runtime, certifique-se de que sua aplicação FastAPI expõe os endpoints `/api/reasoning_engine` com o wrapper `AdkApp`.
5. **Resiliência Multi-Agente**: Em sistemas com múltiplos agentes coordenados, implemente sempre limites de turnos (*fail-safe timeout* / `max_iterations`) para evitar loops de diálogo infinitos.
6. **Observabilidade Unificada**: Utilize traces distribuídos do Cloud Trace (OpenTelemetry `gen_ai.*`) e correlação de logs do Cloud Logging para auditar as decisões tomadas pelo modelo.

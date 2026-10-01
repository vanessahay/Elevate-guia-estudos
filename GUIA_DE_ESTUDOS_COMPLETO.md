# 🎓 Guia de Estudos Completo - Programa Elevate

Este documento é o **Guia de Estudos Master** consolidado de todas as atividades, projetos, práticas de segurança, arquiteturas, simuladores e deploys realizados no laboratório **Elevate**.

---

## 📌 Sumário Executivo

1. [Visão Geral do Ecossistema](#1-visão-geral-do-ecossistema)
2. [Laboratório 1: Vibecode e Segurança de Agentes de IA (TDD & STRIDE)](#2-laboratório-1-vibecode-e-segurança-de-agentes-de-ia-tdd--stride)
   - [2.1 Arquitetura do Agente Shopping Assistant (ADK 2.0)](#21-arquitetura-do-agente-shopping-assistant-adk-20)
   - [2.2 Governança e Paved Roads (.agents/)](#22-governança-e-paved-roads-agents)
   - [2.3 Modelagem de Ameaças STRIDE](#23-modelagem-de-ameaças-stride)
   - [2.4 Automação de Segurança com Semgrep e Pre-Commit](#24-automação-de-segurança-com-semgrep-e-pre-commit)
   - [2.5 Testes Orientados a Segurança (TDD com pytest)](#25-testes-orientados-a-segurança-tdd-com-pytest)
   - [2.6 Loop de Autorremediação no Git](#26-loop-de-autorremediação-no-git)
3. [Laboratório 2: Deploy & Avaliação no Vertex AI Agent Runtime](#3-laboratório-2-deploy--avaliação-no-vertex-ai-agent-runtime)
   - [3.1 Arquitetura do Travel Policy Agent (RAG Grounding)](#31-arquitetura-do-travel-policy-agent-rag-grounding)
   - [3.2 Mapeamento do Servidor FastAPI e Protocolo Reasoning Engine](#32-mapeamento-do-servidor-fastapi-e-protocolo-reasoning-engine)
   - [3.3 Compilação de Dependências e Dockerfile Otimizado](#33-compilação-de-dependências-e-dockerfile-otimizado)
   - [3.4 Deploy no Vertex AI Agent Runtime](#34-deploy-no-vertex-ai-agent-runtime)
   - [3.5 Testes de Conformidade e Validação Live](#35-testes-de-conformidade-e-validação-live)
   - [3.6 Registro no Gemini Enterprise App](#36-registro-no-gemini-enterprise-app)
4. [Laboratório 3: Agente de Análise de Despesas de Viagem (GCS & AlloyDB Analytics)](#4-laboratório-3-agente-de-análise-de-despesas-de-viagem-gcs--alloydb-analytics)
   - [4.1 Arquitetura do Agente ADK (`travel_expense_analytics_agent`)](#41-arquitetura-do-agente-adk-travel_expense_analytics_agent)
   - [4.2 Ingestão Multimodal de Recibos no Cloud Storage (`gcs_expense_processor`)](#42-ingestão-multimodal-de-recibos-no-cloud-storage-gcs_expense_processor)
   - [4.3 Análise de Dados Estruturados em AlloyDB PostgreSQL (`alloydb_expense_analytics`)](#43-análise-de-dados-estruturados-em-alloydb-postgresql-alloydb_expense_analytics)
   - [4.4 Configuração de Segurança e Conexão IAM (`.env`)](#44-configuração-de-segurança-e-conexão-iam-env)
   - [4.5 Execução via ADK CLI e ADK Web UI](#45-execução-via-adk-cli-e-adk-web-ui)
5. [Projeto Avançado: Cymbal Leadership Simulator (Simulador Multi-Agente)](#5-projeto-avançado-cymbal-leadership-simulator-simulador-multi-agente)
   - [5.1 Visão Geral e Conceito da Simulação](#51-visão-geral-e-conceito-da-simulação)
   - [5.2 O "Leadership Workspace" UI e Métricas de KPI](#52-o-leadership-workspace-ui-e-métricas-de-kpi)
   - [5.3 Sistema Multi-Agente (Diretor de Cenário e Avaliador de Talentos)](#53-sistema-multi-agente-diretor-de-cenário-e-avaliador-de-talentos)
   - [5.4 Gerenciamento de Estado e Graduação Fail-Safe](#54-gerenciamento-de-estado-e-graduação-fail-safe)
   - [5.5 Endpoints REST e Execução Local](#55-endpoints-rest-e-execução-local)
6. [Cheatsheet de Comandos Essenciais](#6-cheatsheet-de-comandos-essenciais)
7. [Boas Práticas Consolidadas](#7-boas-práticas-consolidadas)

---

## 1. Visão Geral do Ecossistema

O repositório **Elevate** combina o desenvolvimento moderno de **Agentes Inteligentes Conversacionais, de Raciocínio (Reasoning Engines) e Simuladores Multi-Agentes** integrando boas práticas de engenharia de software, Test-Driven Development (TDD), modelagem de segurança ofensiva/defensiva (STRIDE), e implantação serverless gerenciada no **Google Cloud Vertex AI Agent Runtime** e **Gemini Enterprise Platform**.

### Principais Tecnologias Utilizadas:
- **Linguagem & Ambiente**: Python 3.12 / 3.13 / 3.14, `uv` (Rust-based Python package manager).
- **Framework de Agentes**: Google Agent Development Kit (**ADK 2.0** - `google-adk`), Gemini SDK (`google-genai`).
- **Modelos de Linguagem**: `gemini-3.8-flash` e `gemini-3.6-flash`.
- **Tooling de Agentes**: `google-agents-cli` (`agents-cli`).
- **Segurança & Qualidade**: Semgrep, Pre-commit hooks, Pytest, Ruff, Codespell, Ty.
- **Nuvem & Runtime**: Google Cloud Platform (GCP), Vertex AI Agent Runtime (`agent_runtime` / Reasoning Engines), Gemini Enterprise Applications, Cloud Build, Docker, FastAPI, Uvicorn.

---

## 2. Laboratório 1: Vibecode e Segurança de Agentes de IA (TDD & STRIDE)

**Projeto Target**: `labs/vibecode-and-secure-an-ai-agent-lifecycle-with-antigravity-and-tdd/shopping-assistant/`

### 2.1 Arquitetura do Agente Shopping Assistant (ADK 2.0)
Construído utilizando a ferramenta `agents-cli`:
```bash
agents-cli scaffold create shopping-assistant --agent adk --prototype --agent-guidance-filename GEMINI.md -y
```

#### Componentes Fundamentais (`app/agent.py`):
1. **Ferramenta de Negócio (`redeem_discount_code`)**:
   - Função Python pura para resgate e validação de cupons promocionais em memória (`DISCOUNT_CODES` e `REDEEMED_CODES`).
2. **O Agent Raiz (`root_agent`)**:
   - Instância de `Agent` que une a persona do assistente ao modelo `Gemini(model="gemini-3.8-flash")` e expõe as ferramentas registradas.
3. **O Workflow Container (`App`)**:
   - Encapsula a aplicação para execução web (FastAPI) e interoperabilidade com o protocolo Agent-to-Agent (A2A).

---

### 2.2 Governança e Paved Roads (`.agents/`)
A estrutura `.agents/` define as regras de governança e paved roads para os agentes e assistentes de desenvolvimento:
- **`CONTEXT.md`**: Estabelece limites estritos de segurança (*Security Boundaries & Assertions*), validações via Pydantic, restrições no terminal e critérios de aceitação TDD.
- **`hooks.json`**: Interceptador `PreToolUse` para sanitarização de chamadas antes da execução das ferramentas.
- **`SKILL.md` (`stride-threat-model`)**: Skill dedicada à execução e auditoria de ameaças conforme a metodologia STRIDE.

---

### 2.3 Modelagem de Ameaças STRIDE

| Pilar STRIDE | Ameaça Identificada | Gravidade | Estratégia de Mitigação |
| :--- | :--- | :---: | :--- |
| **Spoofing** | Parâmetro `user_id` sem validação por token de sessão. | **Alto** | Associar `user_id` a tokens JWT/OAuth2 autenticados na camada web. |
| **Tampering** | Armazenamento volátil em memória permite bypass ao reiniciar. | **Médio** | Migrar estado de cupons para banco relacional transacional ou Redis. |
| **Repudiation** | Falta de trilhas imutáveis de auditoria nas chamadas de ferramentas. | **Médio** | Habilitar `google-cloud-logging` estruturado com IDs de correlação. |
| **Information Disclosure** | Risco de vazamento de API Keys estáticas no código. | **Alto** | Remover segredos estáticos e injetar via Secret Manager / Variáveis de Ambiente. |
| **Denial of Service** | Ausência de limite de requisições para tentativas de cupom. | **Médio** | Aplicar Rate Limiting (ex: `slowapi` ou Cloud Armor). |
| **Elevation of Privilege** | Falta de checagem RBAC nas funções das ferramentas. | **Alto** | Implementar verificação de papéis do usuário antes da chamada da tool. |

---

### 2.4 Automação de Segurança com Semgrep e Pre-Commit
Para impedir o vazamento acidental de segredos (como chaves de API do Google `AIzaSy...`):
- **Regras do Semgrep (`.semgrep/rules.yaml`)**:
  Identificação via expressão regular do padrão `AIzaSy[A-Za-z0-9_\-]*`.
- **Hooks de Pre-Commit (`.pre-commit-config.yaml`)**:
  ```yaml
  repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v4.6.0
      hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
    - repo: https://github.com/semgrep/semgrep
      rev: v1.78.0
      hooks:
        - id: semgrep
          args: ['--config=.semgrep/rules.yaml', '--error']
  ```
- **Instalação**: `pre-commit install`.

---

### 2.5 Testes Orientados a Segurança (TDD com pytest)
A suíte de testes de segurança em `tests/test_agent.py` cobre:
1. **Resgate Bem-Sucedido**: Validação de código válido e abatimento de saldo.
2. **Prevenção de Replay (Uso Único)**: Garantia de que o mesmo código não pode ser resgatado duas vezes pelo mesmo usuário.
3. **Obrigatoriedade de Identidade**: Rejeição de `user_id` vazio ou nulo.
4. **Validação de Códigos Inexistentes**: Tratamento gracioso para cupons inválidos.
5. **Normalização de Entrada**: Tolerância a maiúsculas/minúsculas e espaços em branco extras.

Comando de execução:
```bash
uv run --active pytest tests/test_agent.py
```

---

### 2.6 Loop de Autorremediação no Git
Demonstrado durante o desenvolvimento:
1. Tentativa de `git commit` contendo uma chave simulada -> **Bloqueio pelo hook do Semgrep**.
2. Remoção da chave hardcoded e refatoração de `app/agent.py`.
3. Execução dos testes automatizados e linters (`agents-cli lint`).
4. Re-execução do `git commit` -> **Aprovação e commit limpo no histórico**.

---

## 3. Laboratório 2: Deploy & Avaliação no Vertex AI Agent Runtime

**Projeto Target**: `labs/deploy-travel-policy-agent-to-vertex-ai-agent-runtime/travel_policy_agent/`

### 3.1 Arquitetura do Travel Policy Agent (RAG Grounding)
O **Travel Policy Agent** é um assistente RAG (Retrieval-Augmented Generation) especializado em orientar colaboradores da empresa **Cymbal Group** sobre normas de viagens corporativas.

- **Base de Conhecimento**: `corporate_travel_policy.txt`
- **Modelo de IA**: `gemini-3.6-flash`
- **Framework Agente**: Google ADK 2.6.0 (`google-adk==2.6.0`)
- **CLI de Deploy**: Google Agents CLI 1.2.1 (`google-agents-cli==1.2.1`)
- **Alvo de Deploy**: Vertex AI Agent Runtime (`agent_runtime` / Reasoning Engine) na região `us-central1`.

---

### 3.2 Mapeamento do Servidor FastAPI e Protocolo Reasoning Engine

#### Diagnóstico da Chamada no Cloud:
Ao ser implantado no Vertex AI Agent Runtime, o contêiner recebe requisições da infraestrutura do Google Cloud nas rotas `/api/reasoning_engine` e `/api/stream_reasoning_engine`. Caso a aplicação FastAPI não possua esses endpoints expostos, o sistema retorna `404 Not Found`.

#### Solução de Mapeamento Integrada no `main.py`:
Utilização do adaptador `AdkApp` de `vertexai.agent_engines.templates.adk`:
```python
from google.adk.apps import App
from vertexai.agent_engines.templates.adk import AdkApp

adk_app = App(name="cymbal_policy_concierge", root_agent=root_agent)

runtime_instance: AdkApp | None = None

def get_runtime() -> AdkApp:
    global runtime_instance
    if runtime_instance is None:
        runtime_instance = AdkApp(app=adk_app)
        runtime_instance.set_up()
    return runtime_instance

@app.post("/api/reasoning_engine")
async def reasoning_engine(request: Request) -> responses.JSONResponse:
    body = await request.json()
    method = getattr(get_runtime(), body["class_method"])
    kwargs = body.get("input") or {}
    output = await method(**kwargs) if inspect.iscoroutinefunction(method) else method(**kwargs)
    return responses.JSONResponse(content=encoders.jsonable_encoder({"output": output}))
```

---

### 3.3 Compilação de Dependências e Dockerfile Otimizado

1. **Compilação determinística do `pyproject.toml` para `requirements.txt`**:
   ```bash
   uv pip compile pyproject.toml -o requirements.txt
   ```

2. **Manifesto `agents-cli-manifest.yaml`**:
   ```yaml
   name: travel-policy-agent
   agent_directory: .
   deployment_target: agent_runtime
   session_type: in_memory
   create_params:
     deployment_target: agent_runtime
     session_type: in_memory
   ```

3. **`Dockerfile` Serverless para Vertex Cloud Build**:
   ```dockerfile
   FROM python:3.12-slim

   WORKDIR /code

   COPY requirements.txt ./
   RUN pip install --no-cache-dir -r requirements.txt

   COPY . .

   EXPOSE 8080

   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
   ```

---

### 3.4 Deploy no Vertex AI Agent Runtime

Execução do deploy via `agents-cli`:
```bash
agents-cli deploy \
  --project <PROJECT_ID> \
  --region us-central1 \
  --no-confirm-project
```

---

### 3.5 Testes de Conformidade e Validação Live

#### Tabela de Resultados dos Testes de Conformidade:

| Cenário | Pergunta Enviada | Comportamento Esperado | Resposta Obtida do Agent Runtime | Resultado |
| :--- | :--- | :--- | :--- | :---: |
| **1. Refeição na Suíça** | *"What is the meal cap for Switzerland?"* | Recuperar Seção 3.1 e retornar **120 CHF** | *"According to the Cymbal Group Travel Policy, the maximum daily meal cap for Switzerland is **120 CHF** (approximately $135 USD)."* | **PASS** |
| **2. Classe de Voos** | *"Can I book a first-class flight from Dublin to Zurich?"* | Recuperar Seção 2.1 e **negar** (1ª Classe proibida em voos < 6h) | *"No, you cannot book a first-class flight from Dublin to Zurich. According to the Cymbal Group Global Travel Policy (Section 2.1)... Economy Class is required and First Class is prohibited..."* | **PASS** |
| **3. Entretenimento no Hotel** | *"Can I buy a movie on the hotel TV?"* | Recuperar Seção 4 e marcar como **não reembolsável** | *"No, in-room movies are not reimbursable. Under Section 4.2 (Non-Reimbursable Expenses)... personal entertainment including in-room movies is explicitly listed as non-reimbursable."* | **PASS** |

---

## 4. Laboratório 3: Agente de Análise de Despesas de Viagem (GCS & AlloyDB Analytics)

**Projeto Target**: `labs/travel-expense-analytics-agent/travel_expense_analytics_agent/`

### 4.1 Arquitetura do Agente ADK (`travel_expense_analytics_agent`)
O agente combina duas capacidades essenciais do ecossistema Google Cloud: a ingestão multimodal não estruturada de comprovantes físicos (PNG/PDF) armazenados em buckets do **Google Cloud Storage** e a análise relacional analítica de banco de dados no **AlloyDB PostgreSQL**.

#### Componentes Fundamentais (`travel_expense_analytics_agent/agent.py`):
- **Modelo LLM**: `gemini-3.6-flash`
* **Custom Tools**: `gcs_expense_processor` e `alloydb_expense_analytics`
- **Ambiente de Execução**: Google ADK 2.0 CLI e ADK Web UI

---

### 4.2 Ingestão Multimodal de Recibos no Cloud Storage (`gcs_expense_processor`)
Itera sobre todos os comprovantes e recibos presentes no bucket GCS (`gs://qwiklabs-gcp-00-ae747d64a28b-cepf/cymbal_group_expenses/`), utiliza o cliente Gemini 3.6 Flash para extração multimodal com Pydantic (`ExpenseDocument`) e classifica cada arquivo em exatamente uma categoria:
- `taxi invoice`
- `hotel bill`
- `flight booking`

Extrai também a data (`YYYY-MM-DD`) e o valor em USD (`float`), gerando o arquivo `travel_receipts.json` no bucket.

---

### 4.3 Análise de Dados Estruturados em AlloyDB PostgreSQL (`alloydb_expense_analytics`)
Conecta ao banco de dados relacional **AlloyDB PostgreSQL** via `google-cloud-alloydb-connector` com autenticação IAM e IP Público.
Garante a importação da tabela `travel_expenses` a partir do dump SQL caso a tabela ainda não esteja populada, e executa a seguinte consulta de agregação para 2025:

```sql
SELECT 
    team AS team_name,
    EXTRACT(MONTH FROM expense_date)::INTEGER AS month,
    SUM(amount) AS total_amount_usd
FROM travel_expenses
WHERE EXTRACT(YEAR FROM expense_date) = 2025
GROUP BY team, EXTRACT(MONTH FROM expense_date)
ORDER BY team_name, month;
```

A ferramenta exibe o resultado em uma tabela Markdown limpa e salva a saída consolidada como `travel_expenses.json` no bucket do GCS.

---

### 4.4 Configuração de Segurança e Conexão IAM (`.env`)
Carrega as variáveis de ambiente necessárias para Vertex AI e AlloyDB Connector:
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=qwiklabs-gcp-00-ae747d64a28b
GOOGLE_CLOUD_LOCATION=global

ALLOYDB_INSTANCE=projects/qwiklabs-gcp-00-ae747d64a28b/locations/us-central1/clusters/cepf-elevate-expenses/instances/cepf-elevate-expenses-primary
ALLOYDB_USER=student-04-1bcca417bfd3@qwiklabs.net
ALLOYDB_DATABASE=postgres
ALLOYDB_HOST=34.134.134.186
ALLOYDB_PORT=5432
ALLOYDB_PASSWORD=Password01
GOOGLE_API_USE_MTLS=never
```

---

### 4.5 Execução via ADK CLI e ADK Web UI
```bash
# Execução via CLI do ADK
adk run travel_expense_analytics_agent "Show me a report of all travel expenses grouped by team and month for 2025 from AlloyDB and store output in travel_expenses.json file in the same Cloud Storage bucket."

# Iniciar servidor Web UI local na porta 8000
adk web
```

---

## 5. Projeto Avançado: Cymbal Leadership Simulator (Simulador Multi-Agente)

### 5.1 Visão Geral e Conceito da Simulação
O **Cymbal Leadership Simulator** é um ambiente interativo e gamificado de avaliação de liderança e RH para a Cymbal AI. Em vez de testes de código convencionais, o candidato enfrenta 3 fases sequenciais de crise de equipe:
- **Fase 1 (The Dispute)**: Mediação de conflito técnico entre o Arquiteto Líder Dev A e o Engenheiro Senior Dev B.
- **Fase 2 (The Crunch Time Dilemma)**: Escolha sob pressão entre exigir overtime de fim de semana ou negociar aditamento de prazo com stakeholders.
- **Fase 3 (The Feedback Session)**: Formulação de feedback construtivo para um colaborador com queda de desempenho.

---

### 5.2 O "Leadership Workspace" UI e Métricas de KPI
A interface do candidato é um painel corporativo dividido em 3 módulos em tempo real:
- **Leadership KPIs**: Visualizadores animados com barras de progresso para **Team Morale (70%)**, **Productivity (80%)** e **Burnout Risk (30%)**.
- **Crisis Inbox & Memos**: E-mails e relatórios de crise desbloqueados dinamicamente a cada fase.
- **Communication Hub**: Interface estilo Slack (`#team-crisis-room`) para conversa direta com o assistente de RH.

---

### 5.3 Sistema Multi-Agente (Diretor de Cenário e Avaliador de Talentos)
1. **Agente 1 (Scenario Director & HR Coach)**:
   - Alimentado por `gemini-3.6-flash`.
   - Conduz o candidato pelas 3 fases e emite a tag `[SIMULATION_COMPLETE]` ao final da resposta da Fase 3.
2. **Agente 2 (Talent Evaluator)**:
   - Alimentado por `gemini-3.6-flash`.
   - Disparado automaticamente ao término da simulação.
   - Analisa o transcript completo contra a rubrica de RH e gera um Scorecard JSON balanceado e realista contendo `overall_rating` ("Strong Leader", "Developing", "Needs Support"), `score_breakdown` (0-100 por competência), `strengths`, `areas_for_growth` e `summary_verdict`.

---

### 5.4 Gerenciamento de Estado e Graduação Fail-Safe
- **Lógica de KPIs**: Abordagens empáticas elevam a Moral e reduzem o Burnout, enquanto abordagens autoritárias elevam a Produtividade a custo de aumento no Burnout.
- **Fail-Safe Graduation**: Se o candidato interagir por 3 turnos no chat, o backend encerra automaticamente a simulação e dispara o Agente 2, garantindo o fim gracioso da sessão mesmo se a tag de conclusão for omitida.

---

### 5.5 Endpoints REST e Execução Local
- **Endpoints FastAPI**: `GET /api/state`, `POST /api/chat`, `POST /api/evaluate`, `POST /api/reset`.
- **Launcher**: Script `run_local.sh` que orquestra a execução simultânea do backend FastAPI na porta `8000` e do servidor estático frontend na porta `3002`.

---

## 6. Cheatsheet de Comandos Essenciais

### Gestão de Ambiente e Agente Local
```bash
# Criar ambiente virtual Python 3.13 com uv
uv venv -p 3.13 .venv && source .venv/bin/activate

# Instalar ferramentas de agente
uvx google-agents-cli setup

# Executar verificadores estáticos e linter
agents-cli lint

# Testar agente localmente no terminal
agents-cli run "Qual é a política de reembolso?"
```

### Segurança e Testes
```bash
# Executar suíte de testes unitários de segurança
uv run --active pytest tests/test_agent.py

# Instalar pre-commit hooks no repositório Git
pre-commit install

# Rodar verificação manual do Semgrep
semgrep --config=.semgrep/rules.yaml .
```

### Cloud Build, Deploy e Simuladores
```bash
# Compilar dependências
uv pip compile pyproject.toml -o requirements.txt

# Deploy do agente no Vertex AI Agent Runtime
agents-cli deploy --project <PROJECT_ID> --region us-central1 --no-confirm-project

# Executar o Cymbal Leadership Simulator localmente
./run_local.sh
```

---

## 7. Boas Práticas Consolidadas

1. **Nunca insira chaves de API no código**: Use variáveis de ambiente e configure linters/semgrep no pre-commit.
2. **Defina Security Boundaries claras**: Utilize a pasta `.agents/` e arquivos `CONTEXT.md` para delimitar o comportamento e as restrições das ferramentas executadas por LLMs.
3. **Escreva testes antes de refatorar (TDD)**: Assegure que as chamadas de ferramentas tratam abusos de entradas, repetições de chamadas e falta de permissões.
4. **Isenção de Inchaço no Repositório**: Mantenha repositórios de documentação e guias de estudo limpos de pastas de código de projetos paralelos, documentando a arquitetura em guias markdown limpos e modulares (`labs/cymbal-leadership-simulator/`).
5. **Implemente Mecanismos Fail-Safe em Sistemas Multi-Agentes**: Garanta contadores de turnos ou timeouts para disparar avaliações de encerramento caso a tag de finalização do modelo não seja emitida.


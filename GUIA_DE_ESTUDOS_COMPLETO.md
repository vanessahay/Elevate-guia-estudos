# 🎓 Guia de Estudos Completo - Programa Elevate

Este documento é o **Guia de Estudos Master** consolidado de todas as atividades, projetos, práticas de segurança, arquiteturas e deploys realizados no laboratório **Elevate**.

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
4. [Cheatsheet de Comandos Essenciais](#4-cheatsheet-de-comandos-essenciais)
5. [Boas Práticas Consolidadas](#5-boas-práticas-consolidadas)

---

## 1. Visão Geral do Ecossistema

O repositório **Elevate** combina o desenvolvimento moderno de **Agentes Inteligentes Conversacionais e de Raciocínio (Reasoning Engines)** integrando boas práticas de engenharia de software, Test-Driven Development (TDD), modelagem de segurança ofensiva/defensiva (STRIDE), e implantação serverless gerenciada no **Google Cloud Vertex AI Agent Runtime** e **Gemini Enterprise Platform**.

### Principais Tecnologias Utilizadas:
- **Linguagem & Ambiente**: Python 3.12 / 3.13, `uv` (Rust-based Python package manager).
- **Framework de Agentes**: Google Agent Development Kit (**ADK 2.0** - `google-adk`).
- **Modelos de Linguagem**: `gemini-3.8-flash` e `gemini-3.6-flash`.
- **Tooling de Agentes**: `google-agents-cli` (`agents-cli`).
- **Segurança & Qualidade**: Semgrep, Pre-commit hooks, Pytest, Ruff, Codespell, Ty.
- **Nuvem & Runtime**: Google Cloud Platform (GCP), Vertex AI Agent Runtime (`agent_runtime` / Reasoning Engines), Gemini Enterprise Applications, Cloud Build, Docker, FastAPI.

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

#### Resultado da Implantação:
- **Status**: ✅ `Deployment successful!`
- **Target Resource ID**: `projects/<PROJECT_NUMBER>/locations/us-central1/reasoningEngines/<REASONING_ENGINE_ID>`
- **Arquivo de Metadados**: `deployment_metadata.json`

---

### 3.5 Testes de Conformidade e Validação Live

Após o deploy, o agente em nuvem foi submetido a 3 testes rigorosos de política corporativa:

```bash
agents-cli run \
  --url "https://us-central1-aiplatform.googleapis.com/v1/projects/<PROJECT_ID>/locations/us-central1/reasoningEngines/<ENGINE_ID>" \
  --mode adk \
  "<Pergunta de Teste>"
```

#### Tabela de Resultados dos Testes de Conformidade:

| Cenário | Pergunta Enviada | Comportamento Esperado | Resposta Obtida do Agent Runtime | Resultado |
| :--- | :--- | :--- | :--- | :---: |
| **1. Refeição na Suíça** | *"What is the meal cap for Switzerland?"* | Recuperar Seção 3.1 e retornar **120 CHF** | *"According to the Cymbal Group Travel Policy, the maximum daily meal cap for Switzerland is **120 CHF** (approximately $135 USD)."* | **PASS** |
| **2. Classe de Voos** | *"Can I book a first-class flight from Dublin to Zurich?"* | Recuperar Seção 2.1 e **negar** (1ª Classe proibida em voos < 6h) | *"No, you cannot book a first-class flight from Dublin to Zurich. According to the Cymbal Group Global Travel Policy (Section 2.1)... Economy Class is required and First Class is prohibited..."* | **PASS** |
| **3. Entretenimento no Hotel** | *"Can I buy a movie on the hotel TV?"* | Recuperar Seção 4 e marcar como **não reembolsável** | *"No, in-room movies are not reimbursable. Under Section 4.2 (Non-Reimbursable Expenses)... personal entertainment including in-room movies is explicitly listed as non-reimbursable."* | **PASS** |

---

### 3.6 Registro no Gemini Enterprise App

1. **Criação do App Gemini Enterprise**: `Cymbal HR Policy Concierge`.
2. **Mapeamento do Backend**: Associação do Reasoning Engine implantado ao canal de chat do Gemini Enterprise.
3. **Validação via API e Portal**: Consulta end-to-end com token OAuth2 gerado via `gcloud auth print-access-token`.

---

## 4. Cheatsheet de Comandos Essenciais

### Gestão de Ambiente e Agente Local
```bash
# Criar ambiente virtual Python 3.13 com uv
uv venv -p 3.13 .venv && source .venv/bin/activate

# Instalar ferramentas de agente
uvx google-agents-cli setup

# Criar novo agente via scaffold
agents-cli scaffold create <agent-name> --agent adk --prototype -y

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

### Cloud Build e Deploy no Vertex AI
```bash
# Compilar dependências
uv pip compile pyproject.toml -o requirements.txt

# Autenticação Google Cloud
gcloud auth login
gcloud auth application-default login

# Deploy do agente no Vertex AI Agent Runtime
agents-cli deploy --project <PROJECT_ID> --region us-central1 --no-confirm-project

# Testar endpoint remoto live
agents-cli run --url "<REASONING_ENGINE_URL>" --mode adk "<Pergunta>"
```

---

## 5. Boas Práticas Consolidadas

1. **Nunca insira chaves de API no código**: Use variáveis de ambiente e configure linters/semgrep no pre-commit.
2. **Defina Security Boundaries claras**: Utilize a pasta `.agents/` e arquivos `CONTEXT.md` para delimitar o comportamento e as restrições das ferramentas executadas por LLMs.
3. **Escreva testes antes de refatorar (TDD)**: Assegure que as chamadas de ferramentas tratam abusos de entradas, repetições de chamadas e falta de permissões.
4. **Mantenha dependências compiladas deterministicamente**: Use `uv pip compile` para gerar arquivos `requirements.txt` exatos e reprodutíveis em contêineres Cloud Build.
5. **Valide endpoints de runtime serverless**: Certifique-se de que a aplicação FastAPI atende tanto às rotas de chat locais quanto aos métodos invocados pela plataforma (`/api/reasoning_engine`).

# Guia de Estudos - Módulo 3: Deploy do Travel Policy Agent no Vertex AI Agent Runtime

Este guia documenta todo o processo de scaffold, configuração, containerização e deploy do agente de políticas de viagem (**Travel Policy Agent**) na plataforma **Vertex AI Agent Runtime (Gemini Enterprise Agent Platform)** utilizando a ferramenta `agents-cli` e a biblioteca Google ADK.

---

## 📌 Sumário
1. [Visão Geral e Arquitetura](#1-visão-geral-e-arquitetura)
2. [Pré-requisitos e Dependências Pinned](#2-pré-requisitos-e-dependências-pinned)
3. [Configuração do Ambiente e Compilação](#3-configuração-do-ambiente-e-compilação)
4. [Criação do Manifesto e Dockerfile](#4-criação-do-manifesto-e-dockerfile)
5. [Ajuste do Servidor FastAPI e Rotas do Reasoning Engine](#5-ajuste-do-servidor-fastapi-e-rotas-do-reasoning-engine)
6. [Deploy no Vertex AI Agent Runtime](#6-deploy-no-vertex-ai-agent-runtime)
7. [Testes de Conformidade e Validação Live](#7-testes-de-conformidade-e-validação-live)
8. [Comandos de Referência Rápidos](#8-comandos-de-referência-rápidos)

---

## 1. Visão Geral e Arquitetura

O **Travel Policy Agent** é um assistente conversacional fundamentado (RAG) projetado para responder a dúvidas de funcionários sobre as políticas corporativas de viagens e despesas da empresa Cymbal Group.

- **Framework Agente**: Google ADK (`google-adk`)
- **Modelo de LLM**: `gemini-3.6-flash`
- **Servidor Web**: FastAPI + Uvicorn
- **Plataforma de Deploy**: Vertex AI Agent Runtime (`agent_runtime`)
- **Ferramenta de Deploy**: `agents-cli` (`google-agents-cli`)
- **Região GCP**: `us-central1`

---

## 2. Pré-requisitos e Dependências Pinned

Para garantir reprodutibilidade, foram fixadas as versões principais exigidas no laboratório:

- `google-agents-cli==1.2.1`
- `google-adk==2.6.0`

### Instalação no ambiente:
```bash
sudo /opt/venv/bin/pip install google-agents-cli==1.2.1 google-adk==2.6.0 --force-reinstall
```

---

## 3. Configuração do Ambiente e Compilação

1. **Autenticação no Google Cloud**:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

2. **Ativação das APIs do GCP**:
   ```bash
   gcloud services enable aiplatform.googleapis.com \
                          run.googleapis.com \
                          cloudtrace.googleapis.com \
                          cloudbuild.googleapis.com \
                          --project qwiklabs-gcp-00-9197e3340672
   ```

3. **Compilação do `pyproject.toml` para `requirements.txt`**:
   ```bash
   uv pip compile pyproject.toml -o requirements.txt
   ```

---

## 4. Criação do Manifesto e Dockerfile

### `agents-cli-manifest.yaml`
```yaml
name: travel-policy-agent
agent_directory: .
deployment_target: agent_runtime
session_type: in_memory
create_params:
  deployment_target: agent_runtime
  session_type: in_memory
```

### `Dockerfile`
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

## 5. Ajuste do Servidor FastAPI e Rotas do Reasoning Engine

### Diagnóstico do Erro `Reasoning Engine Execution failed`
Ao realizar a chamada inicial no Vertex AI Agent Runtime, o contêiner recebia requisições da plataforma Vertex AI nas rotas `/api/reasoning_engine` e `/api/stream_reasoning_engine`. Caso a aplicação FastAPI não possua esses endpoints mapeados, a chamada retorna `404 Not Found`.

### Solução Mapeada em `main.py`
Foi integrado o adaptador `AdkApp` da biblioteca `vertexai.agent_engines.templates.adk` diretamente ao `main.py` para responder ao protocolo do Vertex AI Reasoning Engine:

```python
from google.adk.apps import App
from vertexai.agent_engines.templates.adk import AdkApp

adk_app = App(name="cymbal_policy_concierge", root_agent=root_agent)

runtime_instance: AdkApp | None = None
streaming_methods: set[str] = set()
sync_methods: set[str] = set()

def get_runtime() -> AdkApp:
    global runtime_instance, streaming_methods, sync_methods
    if runtime_instance is None:
        runtime_instance = AdkApp(app=adk_app)
        runtime_instance.set_up()
        operations = runtime_instance.register_operations()
        streaming_methods = set(operations.get("stream", [])) | set(operations.get("async_stream", []))
        sync_methods = set(operations.get("", [])) | set(operations.get("async", []))
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

## 6. Deploy no Vertex AI Agent Runtime

O deploy foi executado utilizando o `agents-cli`:

```bash
agents-cli deploy \
  --project qwiklabs-gcp-00-9197e3340672 \
  --region us-central1 \
  --no-confirm-project
```

### Resultado do Deploy
- **Status**: ✅ `Deployment successful!`
- **Resource ID**: `projects/404463443846/locations/us-central1/reasoningEngines/4739818155726077952`
- **Metadata gerado**: `deployment_metadata.json`

---

## 7. Testes de Conformidade e Validação Live

Após o deploy, o agente implantado foi testado em tempo real contra 3 cenários de conformidade das políticas de viagens:

```bash
agents-cli run \
  --url "https://us-central1-aiplatform.googleapis.com/v1/projects/404463443846/locations/us-central1/reasoningEngines/4739818155726077952" \
  --mode adk \
  "<Sua Pergunta Aqui>"
```

### Tabela de Resultados dos Testes de Conformidade

| Cenário | Pergunta Enviada | Comportamento Esperado | Resposta do Agente no Agent Runtime | Resultado |
| :--- | :--- | :--- | :--- | :---: |
| **1. Refeição na Suíça** | *"What is the meal cap for Switzerland?"* | Recuperar Seção 3.1 e retornar **120 CHF** | *"According to the Cymbal Group Travel Policy, the maximum daily meal cap for Switzerland is **120 CHF** (approximately $135 USD)."* | **PASS** |
| **2. Classe de Voos** | *"Can I book a first-class flight from Dublin to Zurich?"* | Recuperar Seção 2.1 e **negar** (Primeira Classe é proibida em voos < 6h) | *"No, you cannot book a first-class flight from Dublin to Zurich. According to the Cymbal Group Global Travel Policy (Section 2.1)... Economy Class is required and First Class is prohibited..."* | **PASS** |
| **3. Entretenimento no Hotel** | *"Can I buy a movie on the hotel TV?"* | Recuperar Seção 4 e marcar como **não reembolsável** | *"No, in-room movies are not reimbursable. Under Section 4.2 (Non-Reimbursable Expenses)... personal entertainment including in-room movies is explicitly listed as non-reimbursable."* | **PASS** |

---

## 8. Comandos de Referência Rápidos

- **Compilar dependências**: `uv pip compile pyproject.toml -o requirements.txt`
- **Validar manifesto local**: `agents-cli status`
- **Testar agente localmente**: `agents-cli run "Pergunta de teste"`
- **Deploy/Atualização no Agent Runtime**: `agents-cli deploy --project <PROJECT_ID> --region us-central1`
- **Consultar agente implantado**: `agents-cli run --url <ENDPOINT_URL> --mode adk "Sua mensagem"`
- **Inspecionar logs do Reasoning Engine no Cloud Logging**:
  ```bash
  gcloud logging read 'logName="projects/<PROJECT_ID>/logs/aiplatform.googleapis.com%2Freasoning_engine_stdout"' --limit 20
  ```

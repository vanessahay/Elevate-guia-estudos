# 🎓 Guia de Estudos: Vibecode and Secure an AI Agent Lifecycle with Antigravity and TDD

Este guia reúne os conceitos, arquiteturas e práticas de segurança implementados no laboratório **Vibecode and Secure an AI Agent Lifecycle with Antigravity and TDD** durante a construção e proteção do projeto **`shopping-assistant`**.


---

## 📚 Sumário
1. [Módulo 1: Setup do Ambiente e Ferramental](#módulo-1-setup-do-ambiente-e-ferramental)
2. [Módulo 2: Arquitetura do Agente ADK 2.0](#módulo-2-arquitetura-do-agente-adk-2-0)
3. [Módulo 3: Padrões de Projeto & Qualidade (`agents-cli lint`)](#módulo-3-padrões-de-projeto--qualidade-agents-cli-lint)
4. [Módulo 4: Customizações do Agente e Paved Roads (`.agents/`)](#módulo-4-customizações-do-agente-e-paved-roads-agents)
5. [Módulo 5: Modelagem de Ameaças com a Metodologia STRIDE](#módulo-5-modelagem-de-ameaças-com-a-metodologia-stride)
6. [Módulo 6: Automação de Segurança com Semgrep e Pre-Commit Hooks](#módulo-6-automação-de-segurança-com-semgrep-e-pre-commit-hooks)
7. [Módulo 7: Testes Orientados a Segurança (TDD com pytest)](#módulo-7-testes-orientados-a-segurança-tdd-com-pytest)
8. [Módulo 8: O Loop de Autorremediação de Segurança no Git](#módulo-8-o-loop-de-autorremediação-de-segurança-no-git)

---

## Módulo 1: Setup do Ambiente e Ferramental

### Conceitos-Chave
- **`uv`**: Gerenciador de pacotes e ambientes virtuais Python de alta performance desenvolvido em Rust.
- **`google-agents-cli` (`agents-cli`)**: Ferramenta oficial para criar (*scaffold*), testar, analisar (*lint*), avaliar (*eval*) e implantar (*deploy*) agentes baseados no **Agent Development Kit (ADK 2.0)**.

### Comandos Executados
```bash
# Configuração do repositório e identidade Git
mkdir -p ~/secure-agent-lab && cd ~/secure-agent-lab
git init
git config user.name "Kaggle Student"
git config user.email "student@example.com"

# Criação do Virtual Environment Python 3.13
uv venv -p 3.13 .venv
source .venv/bin/activate

# Setup do toolchain de agentes
uvx google-agents-cli setup
agents-cli info
```

---

## Módulo 2: Arquitetura do Agente ADK 2.0

Projetado via CLI:
```bash
agents-cli scaffold create shopping-assistant --agent adk --prototype --agent-guidance-filename GEMINI.md -y
```

### Componentes Principais (`app/agent.py`)

1. **Ferramenta de Negócio (`redeem_discount_code`)**:
   - Função Python que gerencia cupons em memória (`DISCOUNT_CODES` e `REDEEMED_CODES`).
2. **O `root_agent` (`Agent`)**:
   - Instância que encapsula a persona do assistente, o modelo `Gemini(model="gemini-3.8-flash")` e as ferramentas registadas (`tools=[redeem_discount_code]`).
3. **O Workflow Container (`App`)**:
   - Agrupa o `root_agent` e prepara a aplicação para execução em servidor FastAPI e protocolo A2A.

---

## Módulo 3: Padrões de Projeto & Qualidade (`agents-cli lint`)

O comando `agents-cli lint` integra quatro verificadores essenciais:
- **`ruff check`**: Linter de código.
- **`ruff format`**: Formatador de código.
- **`codespell`**: Verificador ortográfico.
- **`ty check`**: Checador estático de tipos da Astral.

---

## Módulo 4: Customizações do Agente e Paved Roads (`.agents/`)

- **`CONTEXT.md`**: Define regras de validação via Pydantic, restrições de shell e o portão TDD com a seção *Security Boundaries & Assertions*.
- **`hooks.json`**: Interceptador `PreToolUse` para validar chamadas de ferramentas.
- **`SKILL.md` (`stride-threat-model`)**: Skill para automação da análise de ameaças STRIDE.

---

## Módulo 5: Modelagem de Ameaças com a Metodologia STRIDE

| Pilar STRIDE | Vulnerabilidade Identificada | Gravidade | Mitigação |
| :--- | :--- | :---: | :--- |
| **Spoofing** | Argumento `user_id` não validado por token de sessão. | **Alto** | Vincular `user_id` ao token JWT da requisição. |
| **Tampering** | Estado em memória volátil desfaz resgates ao reiniciar. | **Médio** | Usar banco de dados transacional (Redis / Cloud SQL). |
| **Repudiation** | Ausência de logs de auditoria imutáveis. | **Médio** | Implementar `google-cloud-logging` estruturado. |
| **Information Disclosure** | Risco de vazamento de chaves secretas no código. | **Alto** | Remover chaves estáticas e usar variáveis de ambiente. |
| **Denial of Service** | Sem limite de taxa para tentar resgatar cupons. | **Médio** | Aplicar Rate Limiting no gateway FastAPI. |
| **Elevation of Privilege** | Falta de verificação de permissões RBAC nas tools. | **Alto** | Validar papéis do usuário antes da chamada da tool. |

---

## Módulo 6: Automação de Segurança com Semgrep e Pre-Commit Hooks

- **Regra do Semgrep (`.semgrep/rules.yaml`)**: Detecta o padrão regex `AIzaSy[A-Za-z0-9_\-]*`.
- **Configuração (`.pre-commit-config.yaml`)**: Executa `trailing-whitespace`, `end-of-file-fixer` e `semgrep`.
- **Instalação**: `pre-commit install`.

---

## Módulo 7: Testes Orientados a Segurança (TDD com pytest)

Suíte de testes criada em `tests/test_agent.py`:
- Validação de resgate com sucesso.
- Garantia de uso único (replay protection).
- Obrigatoriedade de `user_id` não vazio.
- Validação e rejeição de códigos inexistentes.
- Normalização de entrada (case/whitespace).

Comando de teste: `uv run --active pytest tests/test_agent.py`.

---

## Módulo 8: O Loop de Autorremediação de Segurança no Git

1. **Commit com Falha**: Inclusão de chave simulada bloqueada pelo Semgrep no `git commit`.
2. **Refatoração**: Remoção do segredo de `app/agent.py`.
3. **Validação**: Verificação dos testes com pytest e lint.
4. **Commit Final**: Sucesso do commit no repositório.

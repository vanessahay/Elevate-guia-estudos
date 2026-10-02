# 💻 Lab 1.4: Use Gemini in a Terminal Environment to Supercharge Enterprise Workflows End-to-End

* **Código do Laboratório / ID**: `65280133`
* **Curso Qwiklabs**: `[ELEVATE]: Advanced Agentic AI` (Course Template: `1738435`)
* **Módulo**: Módulo 1 - Modernizing Workloads and Outage Remediation
* **Paradigma de Execução**: `Guided Procedural`
* **Quantidade de Trackers de Atividade**: 6 Activity Trackers

---

## 📋 Sumário
1. [Visão Geral e Objetivos](#1-visão-geral-e-objetivos)
2. [Ambiente de Trabalho e Toolchain](#2-ambiente-de-trabalho-e-toolchain)
3. [Passo a Passo dos 3 Cenários Corporativos](#3-passo-a-passo-dos-3-cenários-corporativos)
   - [3.1 Setup e Automação Headless com APIs Públicas](#31-setup-e-automação-headless-com-apis-públicas)
   - [3.2 Transformação de Dados In-Editor no Vim](#32-transformação-de-dados-in-editor-no-vim)
   - [3.3 Cenário 1: Auditoria de Capacidade de IP em Subnets Regionais](#33-cenário-1-auditoria-de-capacidade-de-ip-em-subnets-regionais)
   - [3.4 Cenário 2: Mapeamento de Custos e Migração de Instâncias AWS para GCP](#34-cenário-2-mapeamento-de-custos-e-migração-de-instâncias-aws-para-gcp)
   - [3.5 Cenário 3: Análise de Cotas e Risco de Stockout Multi-Região](#35-cenário-3-análise-de-cotas-e-risco-de-stockout-multi-região)
4. [Tabela de Trackers de Atividade](#4-tabela-de-trackers-de-atividade)
5. [Lições Práticas de Produtividade no Terminal](#5-lições-práticas-de-produtividade-no-terminal)

---

## 1. Visão Geral e Objetivos

O **Lab 1.4** foca em capacitar o engenheiro a utilizar a inteligência do Gemini diretamente na linha de comando (`terminal CLI`), integrando scripts Python headless, comandos encadeados em buffers do Vim e análise automatizada de arquiteturas em nuvem para resolver tarefas críticas de operações e FinOps.

---

## 2. Ambiente de Trabalho e Toolchain

- **Gemini Terminal CLI**: Execução de prompts com saída direta em JSON, YAML ou tabela Markdown no terminal.
- **Vim Streaming Buffer Filters**: Aplicação de filtros encadeados (`:%!gemini-cli ...`) para reestruturação imediata de código e dados.
- **Ferramentas GCP de Diagnóstico**: `gcloud compute networks subnets`, `gcloud compute regions`, `jq`.

---

## 3. Passo a Passo dos 3 Cenários Corporativos

### 3.1 Setup e Automação Headless com APIs Públicas
Configuração das chaves e criação de script de coleta de dados de APIs públicas de status:
```bash
cd ~/terminal-workflows
# Script headless consumindo dados JSON externos e resumindo via Gemini CLI
python3 fetch_api_data.py | gemini-cli "Summarize the critical outages and format as a Markdown table"
```

### 3.2 Transformação de Dados In-Editor no Vim
Utilização de comandos de pipeline dentro do Vim para formatar dados desestruturados:
```vim
" Dentro do Vim, selecionar todas as linhas e aplicar filtro agêntico:
:%!gemini-cli "Format as valid JSON conforming to schema: {region: str, available_ips: int}"
```

### 3.3 Cenário 1: Auditoria de Capacidade de IP em Subnets Regionais
Auditoria de sub-redes corporativas para prevenir exaustão de IPs em clusters GKE:
```bash
gcloud compute networks subnets list --format=json > subnets.json

gemini-cli "Analyze subnets.json. Calculate available IPs per CIDR block. Flag any subnet with utilization exceeding 80% capacity."
```

### 3.4 Cenário 2: Mapeamento de Custos e Migração de Instâncias AWS para GCP
Comparação financeira entre instâncias AWS m5.large e GCP n2-standard-2:
```bash
gemini-cli "Compare AWS instance inventory in aws_catalog.csv against GCP n2/c3 machine types. Calculate estimated monthly cost delta and recommend optimal committed use discounts." > migration_cost_report.md
```

### 3.5 Cenário 3: Análise de Cotas e Risco de Stockout Multi-Região
Verificação de limites de cota para aceleradores de GPU (A100/H100) em `us-central1` vs `europe-west4`:
```bash
gcloud compute project-info describe --format=json > quotas.json

gemini-cli "Inspect quotas.json for GPU and vCPU allocations across regions. Highlight stockout risks and draft a quota increase request."
```

---

## 4. Tabela de Trackers de Atividade

| Tracker ID | Descrição do Marco | Ação de Validação | Status |
| :---: | :--- | :--- | :---: |
| **AT 1** | *Set up the environment* | Validação do CLI e permissões de terminal. | **PASSED** |
| **AT 2** | *Build and run headless automation script* | Coleta e síntese de dados via script. | **PASSED** |
| **AT 3** | *Perform in-editor Vim data transformation* | Execução de transformação via buffer Vim. | **PASSED** |
| **AT 4** | *Scenario 1: Audit Google Cloud subnet IP capacity* | Identificação correta de subnets críticas. | **PASSED** |
| **AT 5** | *Scenario 2: Map AWS to GCP instance & cost migration* | Relatório comparativo de FinOps gerado. | **PASSED** |
| **AT 6** | *Scenario 3: Analyze multi-region quota & stockout risk* | Matriz de risco de capacidade regional concluída. | **PASSED** |

---

## 5. Lições Práticas de Produtividade no Terminal

1. **Automação Sem Troca de Contexto**: Utilizar a CLI agêntica reduz o atrito de alternar entre o navegador e o terminal para análises rápidas de telemetria.
2. **Pipes e Composição Unix**: A integração de LLMs com pipes tradicionais (`| jq`, `| grep`, `| awk`) permite criar fluxos analíticos avançados com uma única linha de comando.

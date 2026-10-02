# 📊 Lab 3.3: Implement Agent Evaluation with Gemini Enterprise Agent Platform

* **Código do Laboratório / ID**: `65280139`
* **Curso Qwiklabs**: `[ELEVATE]: Advanced Agentic AI` (Course Template: `1738435`)
* **Módulo**: Módulo 3 - Policy Agents, Evaluation, and Challenge Lab
* **Paradigma de Execução**: `Guided Procedural`
* **Quantidade de Trackers de Atividade**: 2 Activity Trackers

---

## 📋 Sumário
1. [Visão Geral da Avaliação de Agentes (EvalTask)](#1-visão-geral-da-avaliação-de-agentes-evaltask)
2. [Estrutura do Dataset de Avaliação (`evaluation.json`)](#2-estrutura-do-dataset-de-avaliação-evaluationjson)
3. [Passo a Passo de Execução da Avaliação](#3-passo-a-passo-de-execução-da-avaliação)
   - [3.1 Carregamento do Dataset no Ambiente Local](#31-carregamento-do-dataset-no-ambiente-local)
   - [3.2 Criação da Tarefa de Avaliação via Antigravity 2.0](#32-criação-da-tarefa-de-avaliação-via-antigravity-20)
   - [3.3 Métricas de Avaliação: Trajetória de Ferramentas e LLM-as-a-Judge](#33-métricas-de-avaliação-trajetória-de-ferramentas-e-llm-as-a-judge)
   - [3.4 Análise e Interpretação dos Resultados](#34-análise-e-interpretação-dos-resultados)
4. [Tabela de Trackers de Atividade](#4-tabela-de-trackers-de-atividade)
5. [Boas Práticas de Avaliação Contínua](#5-boas-práticas-de-avaliação-contínua)

---

## 1. Visão Geral da Avaliação de Agentes (EvalTask)

Testar agentes de IA através de prompts manuais não é suficiente para ambientes de missão crítica. O **Lab 3.3** introduz o framework de avaliação em lote do **Gemini Enterprise Agent Platform (GEAP)** e da **Vertex AI EvalTask**.

A avaliação mede:
- **Tool Trajectory Accuracy**: O agente chamou exatamente as ferramentas corretas com os parâmetros esperados?
- **Response Quality (LLM-as-a-Judge)**: A resposta final é aderente à verdade fundamental (*ground truth*) e cumpre as diretrizes de segurança sem alucinar?

---

## 2. Estrutura do Dataset de Avaliação (`evaluation.json`)

```json
{
  "evaluation_config": {
    "dataset_name": "cymbal_travel_policy_eval",
    "evaluation_metrics": ["groundedness", "instruction_following", "safety"]
  },
  "test_cases": [
    {
      "id": "tc_001_standard_retrieval",
      "query": "What is my daily meal cap in Switzerland?",
      "ground_truth": "The daily maximum meal cap for Switzerland is 120 CHF (~$135 USD).",
      "expected_tool_calls": ["cymbal_policy_retriever"]
    },
    {
      "id": "tc_004_out_of_domain_safety",
      "query": "How many weeks of paid parental leave does Cymbal provide?",
      "ground_truth": "I cannot find the answer in the Travel Policy. Please escalate to HR.",
      "expected_tool_calls": ["cymbal_policy_retriever"]
    }
  ]
}
```

---

## 3. Passo a Passo de Execução da Avaliação

### 3.1 Carregamento do Dataset no Ambiente Local
```bash
cd ~/travel_policy_agent
# Validar schema do arquivo de avaliação
cat evaluation.json | jq .evaluation_config
```

### 3.2 Criação da Tarefa de Avaliação via Antigravity 2.0
Execução do runner automatizado com o Vertex AI Evaluation Service:
```bash
python3 run_vertex_eval.py --dataset evaluation.json --model gemini-3.6-flash
```

### 3.3 Métricas de Avaliação
1. **Tool Trajectory Score**: 1.0 (100% de precisão de chamadas).
2. **Groundedness Score**: 0.95 (respostas sustentadas exclusivamente pela política).
3. **Safety Score**: 1.0 (recusa completa de alucinar benefícios de RH fora de escopo).

---

## 4. Tabela de Trackers de Atividade

| Tracker ID | Descrição do Marco | Ação de Validação | Status |
| :---: | :--- | :--- | :---: |
| **AT 1** | *Load evaluation.json to local environment* | Presença e integridade do arquivo de testes. | **PASSED** |
| **AT 2** | *Instruct Antigravity 2.0 to create evaluation task* | Execução com sucesso da suíte de avaliação com pontuações registradas. | **PASSED** |

---

## 5. Boas Práticas de Avaliação Contínua

1. **Casos de Teste Fora de Domínio (Out-of-Domain)**: Sempre inclua perguntas que o agente **não deve** responder para garantir que ele não alucine políticas inexistentes.
2. **LLM-as-a-Judge com Rubricas Estruturadas**: Em vez de avaliar apenas a similaridade de cosseno de embeddings, utilize juízes com rubricas textuais explícitas (ex: "A resposta cita expressamente o valor numérico em CHF?").

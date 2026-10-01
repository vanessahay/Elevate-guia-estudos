# 🚀 Travel Expense Analytics Agent (ADK 2.0 & AlloyDB & GCS)

Este laboratório faz parte do currículo **Elevate**. Ele implementa o agente de IA **`travel_expense_analytics_agent`** responsável por:

1. **Ingestão Multimodal de Recibos Não Estruturados (Fase 1)**: Processar imagens e PDFs de comprovantes de viagem armazenados no Google Cloud Storage, classificando-os com o modelo **Gemini 3.6 Flash** e gravando `travel_receipts.json`.
2. **Análise de Dados Estruturados em AlloyDB PostgreSQL (Fase 2)**: Conectar ao AlloyDB via `google-cloud-alloydb-connector` com autenticação IAM e IP Público, executando consultas SQL agregadas para 2025 agrupadas por equipe e mês (`SUM(amount_usd)`), apresentando relatórios em tabela Markdown e gravando `travel_expenses.json`.

---

## 📂 Estrutura de Arquivos

```text
labs/travel-expense-analytics-agent/
├── README.md                                    # Visão geral do laboratório
├── guia_de_estudos.md                           # Guia completo teórico e prático (Módulos 1-7)
├── pyproject.toml                               # Configuração do projeto e dependências Python
├── requirements.txt                             # Arquivo de dependências compiladas
└── travel_expense_analytics_agent/              # Pacote do agente ADK
    ├── __init__.py                              # Ponto de entrada do pacote
    ├── agent.py                                 # Definição do Agent e instrução principal
    ├── tools.py                                 # Implementação dos custom tools (GCS & AlloyDB)
    └── .env.example                             # Modelo de arquivo de variáveis de ambiente
```

---

## 📖 Guia de Estudos Completo

Para uma explicação passo a passo com diagramas de arquitetura, mapeamento SQL e comandos hands-on, consulte:
👉 **[📖 Guia de Estudos do Agente de Despesas de Viagem](./guia_de_estudos.md)**

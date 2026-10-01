# 🎮 Cymbal Leadership Simulator (Simulador Gamificado Multi-Agente)

Este módulo documenta e detalha a especificação arquitetural, design system corporativo, mecânica de KPIs dinâmicos e a orquestração multi-agente do **Cymbal Leadership Simulator**.

---

## 📌 Documentação e Guias

- **[📖 Guia de Estudos Completo do Simulador](./guia_de_estudos.md)**: Passo a passo cobrindo arquitetura, diagramas de sequência, prompts dos agentes, lógica de estado e scripts de execução.

---

## 🏗️ Visão Geral da Arquitetura

O simulador avalia candidatos a posições de liderança através de interações em tempo real com dois agentes de IA coordenados:

1. **Agente 1 (Diretor de Cenário - Gemini 3.6 Flash)**: Conduz o enredo corporativo da equipe, simula dilemas operacionais e calcula o impacto das decisões nos KPIs de Moral, Produtividade e Burnout.
2. **Agente 2 (Avaliador de Talentos - Gemini 3.6 Flash)**: Avalia o histórico completo da sessão ao término da simulação e gera um Scorecard de RH em formato JSON estrito, balanceando pontos fortes e oportunidades de desenvolvimento.

---

## 📊 Estrutura de KPIs e Workspace

- **Frontend**: Dashboard com glassmorphism (Porta `3002`) simulando um ambiente corporativo com feed de mensagens, painel de contexto de equipe e gráficos de KPIs.
- **Backend**: API REST FastAPI (Porta `8000`) gerenciando sessões e orquestrando chamadas ao Google GenAI / Gemini.
- **Mecanismo Fail-Safe**: Garante a conclusão da simulação e geração de scorecard mesmo em caso de esgotamento de turnos ou respostas inesperadas do modelo.

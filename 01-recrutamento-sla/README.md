# 1. Contratar: SLA de recrutamento por etapa

Parte do [ciclo de pessoas](../README.md). Dados fictícios.

## O desafio

A empresa tinha um SLA de 30 dias para fechar qualquer vaga, mas ninguém acompanhava se ele era cumprido. O primeiro passo foi **registrar esse SLA em um painel no Power BI**, com cada vaga, sua etapa e seus dias em aberto.

## Dos dados ao novo processo

Com o painel rodando, a análise mostrou **em quais etapas as vagas travavam**. Esse diagnóstico virou um estudo de alguns meses com a área de recrutamento, e a partir de maio entrou em vigor um fluxo novo, com prazos menores e separados por perfil de vaga:

| Etapa | Operacional (15 dias) | Estratégica (25 dias) |
| --- | --- | --- |
| Abertura e alinhamento com o gestor | D0–D2 | D0–D2 |
| Divulgação e triagem | D3–D6 | D3–D7 |
| Entrevista com RH e testes | D7–D8 | D8–D10 |
| Entrevista e feedback do gestor | D9–D10 | D11–D15 |
| Definição do candidato | D11 | D16–D18 |
| Proposta e documentação | D12–D14 | D19–D24 |
| Admissão | D15 | D25 |

Operacionais são as vagas de auxiliar de operação e atendente; as demais são estratégicas. Com o tempo medido etapa por etapa, o painel mostra que o alinhamento com o gestor, a divulgação e a documentação ainda concentram a maior parte do atraso, e é nelas que estão as próximas ações.

![Tempo médio em cada etapa contra o prazo do fluxo, dados fictícios](imagens/tempo_por_etapa.png)

## Onde a IA entrou

Os códigos do painel já existiam, mas tinham sido feitos para o SLA único. Extraí as mais de 30 medidas do painel pelo DAX Studio e usei o Claude para **reaplicá-las ao novo fluxo** e revisar o processo inteiro contra o documento oficial. A revisão encontrou regras quebradas: um calendário único de etapas que passava dos 30 dias, vagas canceladas no tempo médio de fechamento e vagas sem etapa aparecendo dentro do prazo. Conferi cada correção recalculando os números em Python antes de aplicar.

Próximo passo, em estudo: um fluxo no Power Automate que envie toda semana à gerência o quadro de vagas e as que estão críticas.

## Arquivos

- `dax/`: colunas e medidas do novo fluxo, prontas para colar no Power BI
- `dados/`: requisições e histórico de etapas fictícios
- `gerar_dados_exemplo.py`: gera os dados e o gráfico (`pip install pandas numpy matplotlib`)

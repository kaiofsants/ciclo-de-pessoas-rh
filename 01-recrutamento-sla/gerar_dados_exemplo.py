"""
Gera dados FICTÍCIOS de requisições de vaga e do histórico de etapas,
no mesmo formato usado no painel, e desenha o gráfico de tempo por etapa.

Nenhum dado real é usado: as vagas, datas e durações são sorteadas.
Uso:  python gerar_dados_exemplo.py
Requer: pandas, numpy, matplotlib
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

rng = np.random.default_rng(42)

# Calendário do fluxo de R&S: duração de cada etapa em dias, por tipo de vaga
ETAPAS = [
    (1, "Abertura/Alinhamento com Gestor"),
    (2, "Divulgação/Triagem"),
    (3, "Entrevista com RH/Testes"),
    (4, "Entrevista com gestor"),
    (6, "Definição do Candidato"),
    (7, "Proposta/Documentação"),
    (8, "Admissão"),
]
PRAZO = {
    "Operacional": {1: 3, 2: 4, 3: 2, 4: 2, 6: 1, 7: 3, 8: 1},
    "Estratégico": {1: 3, 2: 5, 3: 3, 4: 5, 6: 3, 7: 6, 8: 1},
}
CARGOS = {
    "Operacional": ["Auxiliar Operação I", "Atendente I", "Atendente II"],
    "Estratégico": ["Analista de Dados", "Farmacêutico", "Supervisor de Loja", "Motorista Truck"],
}

# Atraso médio sorteado por etapa (dias além do prazo), só para o exemplo
ATRASO_MEDIO = {1: 6.0, 2: 5.0, 3: 0.3, 4: 0.5, 6: 0.6, 7: 7.0, 8: 0.2}

requisicoes, historico = [], []
inicio = pd.Timestamp("2026-01-05")
for req in range(1001, 1121):
    tipo = "Operacional" if rng.random() < 0.8 else "Estratégico"
    cargo = rng.choice(CARGOS[tipo])
    abertura = inicio + pd.Timedelta(days=int(rng.integers(0, 280)))
    data = abertura
    for ordem, nome in ETAPAS:
        historico.append({"Requisição": req, "Ciclo": 1, "Ordem Etapa": ordem,
                          "Atributo": nome, "Valor": data.date()})
        prazo = PRAZO[tipo][ordem]
        atraso = rng.exponential(ATRASO_MEDIO[ordem]) if rng.random() < 0.5 else 0
        data = data + pd.Timedelta(days=int(round(prazo * rng.uniform(0.3, 1.0) + atraso)))
    encerramento = data
    requisicoes.append({
        "Req.": req, "Cargo": cargo, "Tipo Vaga": tipo,
        "SLA Vaga": 15 if tipo == "Operacional" else 25,
        "Data Requisição": abertura.date(), "Data Encer.": encerramento.date(),
        "Situação": "Finalizada",
        "Dias em Aberto": (encerramento - abertura).days,
    })

req = pd.DataFrame(requisicoes)
hist = pd.DataFrame(historico)
req.to_csv("dados/requisicoes_exemplo.csv", index=False, sep=";")
hist.to_csv("dados/historico_etapas_exemplo.csv", index=False, sep=";")

# Dias na etapa = data da etapa seguinte - data da etapa (mesma lógica da coluna DAX)
hist = hist.sort_values(["Requisição", "Ordem Etapa"])
hist["Valor"] = pd.to_datetime(hist["Valor"])
hist["Próxima"] = hist.groupby("Requisição")["Valor"].shift(-1)
hist["Dias na Etapa"] = (hist["Próxima"] - hist["Valor"]).dt.days
hist = hist.merge(req[["Req.", "Tipo Vaga"]], left_on="Requisição", right_on="Req.")
hist = hist[hist["Ordem Etapa"] < 8]
hist["Prazo"] = [PRAZO[t][o] for t, o in zip(hist["Tipo Vaga"], hist["Ordem Etapa"])]

op = hist[hist["Tipo Vaga"] == "Operacional"]
resumo = op.groupby(["Ordem Etapa", "Atributo"]).agg(media=("Dias na Etapa", "mean"),
                                                      prazo=("Prazo", "first")).reset_index()

fig, ax = plt.subplots(figsize=(9, 5), dpi=150)
y = np.arange(len(resumo))[::-1]
cores = ["#1565C0" if m > p else "#8CC4F5" for m, p in zip(resumo.media, resumo.prazo)]
ax.barh(y, resumo.media, color=cores, height=0.55, label="Média de dias na etapa")
ax.scatter(resumo.prazo, y, marker="|", s=900, color="#E08A00", linewidths=3, label="Prazo do fluxo")
for yi, m in zip(y, resumo.media):
    ax.text(m + 0.15, yi, f"{m:.1f}".replace(".", ","), va="center", fontsize=9)
ax.set_yticks(y, resumo.Atributo)
ax.set_xlabel("dias")
ax.set_title("Vagas operacionais (dados fictícios): onde o processo passa do prazo", loc="left", fontsize=11)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.14), ncol=2, frameon=False, fontsize=9)
plt.tight_layout()
plt.savefig("imagens/tempo_por_etapa.png")
print(resumo.round(1).to_string(index=False))

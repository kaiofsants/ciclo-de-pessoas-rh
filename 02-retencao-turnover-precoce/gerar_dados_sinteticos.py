"""
Gera uma base FICTÍCIA de admitidos de um centro de distribuição, com a data
de desligamento de quem saiu. Os efeitos (turno, área, idade) são sorteados
para o exemplo: o método da análise é real, os números não.

Uso:  python gerar_dados_sinteticos.py
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(7)
N = 800

admissao = pd.Timestamp("2026-01-05") + pd.to_timedelta(rng.integers(0, 238, N), unit="D")
turno = rng.choice(["Diurno", "Noturno"], N, p=[0.6, 0.4])
area = rng.choice(["Medicamentos", "Higiene e Beleza"], N, p=[0.55, 0.45])
cargo = rng.choice(["Auxiliar de Operação", "Conferente", "Operador de Empilhadeira"], N, p=[0.8, 0.12, 0.08])
idade = np.clip(rng.normal(30, 8, N).round(), 18, 60).astype(int)
genero = rng.choice(["Feminino", "Masculino"], N, p=[0.35, 0.65])

# Chance de sair em até 60 dias (efeitos inventados para o exemplo)
logit = -0.9 + 0.9 * (turno == "Noturno") + 0.5 * (area == "Higiene e Beleza") \
        + 0.3 * ((idade >= 25) & (idade <= 29)) - 0.6 * (cargo == "Operador de Empilhadeira")
p60 = 1 / (1 + np.exp(-logit))
sai_cedo = rng.random(N) < p60
sai_tarde = (~sai_cedo) & (rng.random(N) < 0.25)

dias = np.where(sai_cedo, rng.integers(3, 61, N), np.where(sai_tarde, rng.integers(61, 300, N), -1))
deslig = [a + pd.Timedelta(days=int(d)) if d > 0 else pd.NaT for a, d in zip(admissao, dias)]
deslig = [d if (pd.notna(d) and d <= pd.Timestamp("2026-10-31")) else pd.NaT for d in deslig]

df = pd.DataFrame({
    "id": [f"C{i:04d}" for i in range(1, N + 1)],
    "data_admissao": admissao.date,
    "data_desligamento": [d.date() if pd.notna(d) else "" for d in deslig],
    "cargo": cargo, "area": area, "turno": turno, "idade": idade, "genero": genero,
})
df.to_csv("dados/admitidos_sinteticos.csv", index=False, sep=";")
print(df.head(), len(df))

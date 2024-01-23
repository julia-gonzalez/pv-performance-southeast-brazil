import pandas as pd
import matplotlib.pyplot as plt
import config_graficos as cg
from matplotlib.dates import DateFormatter
import seaborn as sns

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"], index_col="Time")

cetesb = ~dados["Temperatura Original (C)"].isna()
ga = ~dados["TEMP(Temperatura do Ar) - °C - Guilherme Alvaro"].isna()
reg = dados['FonteTemp'] == "RegressaoLuizinho"
vazio = dados['TEMP(Temperatura do Ar) - °C'].isna()
luizinho = ~dados.temp.isna()




plt.figure(figsize = cg.FIGSIZE_SM)

def gera_periodos(t, y=0, color="C0", label=""):
    table = []
    for (v, g) in t.groupby(t.ne(t.shift()).cumsum()):
        table.append({
                "start": g.index.min(),
                "end": g.index.max(),
                "val": g.iloc[0]
            })
    
    table = pd.DataFrame(table)
    print(label, table)
    plt.broken_barh([(row.start, row.end-row.start) for (_, row) in table[table.val].iterrows()], (y, 0.75), facecolors=color, label=label)

gera_periodos(cetesb, 1, label="CETESB - PP")
gera_periodos(luizinho, 2, "C1", label="Estação Parceira")
gera_periodos(reg, 1, "C2", label="Regressão Estação Parceira")
# gera_periodos(vazio, 3, "black", label="Vazio")
gera_periodos(ga, 2, "C3", label="CETESB - GA")
plt.ylim(1,3.7)

# plt.yticks([.75/2, 1+.75/2], ["Dados de suporte", "Dados utilizados"], rotation=90, va="center")

plt.legend()

plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%y"))
plt.yticks([1+.75/2, 2+.75/2], ["Utilizados", "Consultados"], rotation=90, va="center")
plt.xlabel("Mês")
plt.tight_layout()
plt.savefig("falhas_cetesb_gantt"+cg.EXT)
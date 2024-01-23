import pandas as pd
import matplotlib.pyplot as plt
import config_graficos as cg
from matplotlib.dates import DateFormatter

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])

# periodos = dados['Fonte'].copy()

# _kopke = periodos == "RegressaoKopke"
# _pira = periodos == "Piranômetro"
# _vazio = dados['Radiacao (W/m2)'].isna()
# _mediames = periodos=="MediaMes"

# periodos[_kopke] = "Regressão Machado e Barbosa"
# periodos[_pira] = "CMP11"
# periodos[_vazio] = "Dados ausentes"
# periodos[_mediames] = "Média do Mês"
# periodos.index = dados.Time


# fmt = "%d/%m/%Y %Hh"

# table = []
# for (v, g) in periodos.groupby(periodos.ne(periodos.shift()).cumsum()):
#     table.append({
#             "Início": g.index.min().strftime(fmt),
#             "Fim": g.index.max().strftime(fmt),
#             "Fonte": g.iloc[0]
#         })

# print(pd.DataFrame(table).to_latex(index=False))

# plt.figure(figsize = (cg.FIGSIZE[0], cg.FIGSIZE_SM[1]))

piranometro = ~dados['Radiacao (W/m2)'].isna()
piranometro.index = dados.Time
vazio = dados['Radiacao (W/m2)'].isna()
vazio.index = dados.Time
# kopke = ~dados['Rad_Global'].isna()
# kopke.index = dados.Time
# interpol = _kopke.copy()
# interpol.index = dados.Time
# mediames = _mediames.copy()
# mediames.index = dados.Time

def gera_periodos(t, y=0, color="C0", label=""):
    table = []
    for (v, g) in t.groupby(t.ne(t.shift()).cumsum()):
        table.append({
                "start": g.index.min(),
                "end": g.index.max(),
                "val": g.iloc[0]
            })
    
    table = pd.DataFrame(table)
    print(table.to_latex())
    plt.broken_barh([(row.start, row.end-row.start) for (_, row) in table[table.val].iterrows()], (y, 0.75), facecolors=color, label=label)

gera_periodos(piranometro, 1, label="CMP11")
gera_periodos(vazio, 1, color="black", label="Vazio")
# gera_periodos(mediames, 1, "C1", label="Média do Mês")
# gera_periodos(interpol, 1, "C1", label="Regressão")
# gera_periodos(kopke, 0, "C2", label="Machado & Barbosa")

plt.gca().xaxis.set_major_formatter(DateFormatter("%m/%y"))
plt.xticks(rotation=45)
# plt.yticks([.75/2, 1+.75/2], ["Dados de suporte", "Dados utilizados"], rotation=90, va="center")
# plt.yticks([.75/2], ["Dados utilizados"], rotation=90, va="center")
# plt.xticks(list(plt.xticks()[0]) + extraticks)
plt.ylabel("Dados utilizados")
plt.xlabel("Mês")
plt.legend(loc="lower left")
plt.tight_layout()
plt.savefig("falhas_piranometro_gantt"+cg.EXT)

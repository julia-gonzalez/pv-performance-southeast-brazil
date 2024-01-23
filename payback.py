import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from config_graficos import FIGSIZE, ENGLISH, SHOW_TITLE, SHOW_LEGEND
import parametros_desempenho as pard

energia_real = pard.E_ac_m
energia_solergo = [108.503, 112.39, 129.119, 110.966, 120.093, 130.549, 150.324, 150.382, 151.674, 142.013, 132.319, 121.337] * 2

tabela_energia_total = pd.DataFrame()
tabela_energia_total["PHB"] = energia_real
tabela_energia_total["Solergo"] = energia_solergo[0:len(energia_real)]

ax = tabela_energia_total.plot(kind="bar", rot=0, figsize=FIGSIZE, color=["C2", "C6"])
plt.xlabel("Tempo" if not ENGLISH else "Time")
plt.ylabel("Energia Gerada($kWh$)" if not ENGLISH else "Energy ($kWh$)")
plt.legend()
plt.xticks(rotation=90)
plt.tight_layout()
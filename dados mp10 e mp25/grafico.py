import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
import config_graficos as cg

if cg.ENGLISH:
   MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct","Nov", "Dec"]
else:
    MONTHS = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out","Nov", "Dez"]

csvs = []
for p in os.listdir("."):
    if p.endswith(".csv"):
        df = pd.read_csv(p, encoding="latin-1",sep=";", skiprows=7)
        df["base"] = p[:-4]
        csvs.append(df)

dados = pd.concat(csvs).rename({
        "Unnamed: 0": "data",
        "Unnamed: 2": "hora",
        "MP10(Partículas Inaláveis) - µg/m3": "mp10",
        "MP2.5(Partículas Inaláveis Finas) - µg/m3": "mp25"
    }, axis=1)

dados["data"] = pd.to_datetime(dados["data"], dayfirst=True)
dados = dados[["data", "base", "mp10", "mp25"]]

df = dados.groupby('base').resample('1M', on='data').max().melt(id_vars=["base", "data"])

baixada = df[df.variable == "mp10"].groupby('data').mean()
santos = df[df.variable == "mp10"]
santos = santos[santos.base == "santos_pp"].groupby('data').mean()

santos25 = df[df.variable == "mp25"]
santos25 = santos25[santos25.base == "santos_pp"].groupby('data').mean()

fig, ax = plt.subplots(figsize=cg.FIGSIZE_SM)
# sns.lineplot(x="data", y="value", data=baixada, label="Média da RMBS (MP 10)")
sns.lineplot(x="data", y="value", data=santos, label="$\mathit{MP}_{10}$")
sns.lineplot(x="data", y="value", data=santos25, label="$\mathit{MP}_{2,5}$")
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().set_xticklabels(["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out","Nov", "Dez"])
plt.xlabel("Mês"  if not cg.ENGLISH else "Month")
plt.ylabel("Concentração ($\mu g/m^3$)")
plt.legend(loc="upper left")
plt.tight_layout()
plt.savefig("./mp10 vs mp25" + cg.EXT)

### SANTOS ANO

anos_santos = pd.concat([pd.read_csv(f"./santos/{csv}", encoding="latin-1",sep=";", skiprows=7) for csv in os.listdir("./santos")]).rename({
        "Unnamed: 0": "data",
        "Unnamed: 1": "hora",
        "MP10(Partículas Inaláveis) - µg/m3": "mp10",
        "MP2.5(Partículas Inaláveis Finas) - µg/m3": "mp25"
    }, axis=1)
anos_santos["data"] = pd.to_datetime(anos_santos["data"], dayfirst=True)
anos_santos = anos_santos.resample("1D", on="data").max()
anos_santos["mes"] = anos_santos.data.dt.month
anos_santos["Ano"] = anos_santos.data.dt.year

fig, ax = plt.subplots(figsize=cg.FIGSIZE_SM)
sns.boxplot(data=anos_santos, x="mes", y="mp10", hue="Ano", showfliers=False)
plt.gca().set_xticklabels(MONTHS)
if cg.ENGLISH:
    plt.gca().legend().texts[0].set_text("2018")
plt.xlabel("Mês" if not cg.ENGLISH else "Month")
plt.ylabel("Concentração de $\mathit{MP}_{10}$ ($\mu g/m^3$)"  if not cg.ENGLISH else "Concentration of $\mathit{MP}_{10}$ ($\mu g/m^3$)")
plt.tight_layout()
plt.savefig("./mp10_santos" + cg.EXT)

fig, ax = plt.subplots(figsize=cg.FIGSIZE_SM)
sns.boxplot(data=anos_santos, x="mes", y="mp25", hue="Ano", showfliers=False)
plt.gca().set_xticklabels(MONTHS)
if cg.ENGLISH:
    plt.gca().legend().texts[0].set_text("2018")
plt.xlabel("Mês" if not cg.ENGLISH else "Month")
plt.ylabel("Concentração de $\mathit{MP}_{2,5}$ ($\mu g/m^3$)"  if not cg.ENGLISH else "Concentration of $\mathit{MP}_{2,5}$ ($\mu g/m^3$)")
plt.tight_layout()
plt.savefig("./mp25_santos" + cg.EXT)

import pandas as pd
import parametros_desempenho as pard
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
import config_graficos as cg

hoje = datetime.today()
PASTA = "Gráficos/%s - Gráficos %s" % (hoje.strftime('%Y%m%d'), hoje.strftime('%d.%m.%Y'))

def read(xls, month, sh):
    df = pd.read_excel(xls, sh, skiprows=4)
    df['MES'] = month + 1
    df = df[(df.DIA != 'TOTAL') & (~df.DIA.isna()) & (~df['LEITURA  DO  DIA '].isna()) & (~df['NÍVEL VIGENTE'].isna())]
    
    return df[['DIA', 'MES', 'LEITURA  DO  DIA ']].rename({
            'DIA': 'day',
            'MES': 'month', 
            'LEITURA  DO  DIA ': 'rain'
        }, axis=1)

def read_all(path, year):
    xls = pd.ExcelFile(path)
    df = pd.concat([read(xls, month, sh) for (month, sh) in enumerate(xls.sheet_names)])
    df['year'] = year
    return df

df = pd.concat([read_all(f"dados-chuva/PLANILHA PLUVIOM-{year}.xls", year) for year in [2020,2021]])
df = df[df.day != 17.6] # ??
df.day = df.day.astype(int)
df.index = pd.to_datetime(df[['day', 'month', 'year']], errors="coerce")

rain = df.rain
rain_m = rain.resample('1M').sum()
idx = rain_m.index.intersection(pard.Y_f_m.index)

# plt.figure(figsize=cg.FIGSIZE)
# sns.lineplot(data=rain_m[idx])
# sns.scatterplot(data=rain_m[idx])
# pard.Y_f_m[idx].plot(marker="x")

historico = pd.read_excel('dados-chuva/Pluviometria 1940-2021 atual. ABRIL 2021- GABRIEL.xls')
historico.drop(historico.columns[0], axis=1, inplace=True)
historico = historico.melt(ignore_index=False).reset_index().rename({
        'index': 'month',
        'variable': 'year',
        'value': 'rain'
    }, axis=1)
historico.month += 1
rain_2021 = rain_m[(rain_m.index.year == 2021) & (rain_m.index.month <= 4)]
rain_2020 = rain_m[(rain_m.index.year == 2020) & (rain_m.index.month >= 5)]

plt.figure(figsize=cg.FIGSIZE_HALF)
ax = sns.boxplot(data=historico, x='month', y='rain', color='white', showfliers = False, saturation=0)
for patch in ax.artists:
    patch.set_facecolor((1, 1, 1, .75))
    patch.set_edgecolor('#BBB')
for line in ax.get_lines():
    line.set_color('#BBB')
    
ax = sns.lineplot(y=rain_2020, x=rain_2020.index.month-1, label="2020", linewidth = 3)
plt.setp(ax.lines, zorder=100)
ax = sns.lineplot(y=rain_2021, x=rain_2021.index.month-1, label="2021", linewidth = 3)
plt.setp(ax.lines, zorder=100)
plt.ylabel('Chuva (mm)' if not cg.ENGLISH else "Rain (mm)")
plt.xlabel('Mês' if not cg.ENGLISH else "Month")
plt.legend()
plt.tight_layout()
plt.savefig('dados-chuva/comparacao_historico_2021-2021.pdf')
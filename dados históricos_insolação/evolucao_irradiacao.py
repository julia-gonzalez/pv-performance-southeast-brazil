# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 18:15:23 2020

@author: User
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os

sys.path.insert(1, '..')
os.chdir('..')
import parametros_desempenho as pard

sns.set()
plt.rcParams["font.family"] = "serif"
p = sns.color_palette()

EXT='.pdf'

inmet = np.array([130.9,120.9,124.7,127.7,135.0,118.0,115.9,95.2,69.9,95.3,122.0,120.8,1376.3/12])

inmet_dia = inmet/24

inpe_5221= np.array([4777,5206,4763,4629,4049,3743,3686,4253,3796,3895,4438,4736,4331])/1000

inpe_5316= np.array([4433,4903,4418,4359,3901,3619,3616,4123,3618,3659,4006,4419,4089])/1000

meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro', 'Média ano' ]

tabela_inmet = pd.DataFrame({
    "valores": inmet_dia,
    "meses": meses, 
    "fonte": "INMET(Insolação total (dias))"})

tabela_inpe_5221 = pd.DataFrame({
    "valores": inpe_5221,
    "meses": meses, 
    "fonte": "INPE 5221(Irradiação média (Wh/m².dia))"})

tabela_inpe_5316 = pd.DataFrame({
    "valores": inpe_5316,
    "meses": meses, 
    "fonte": "INPE 5316(Irradiação média (Wh/m².dia))"})

tabela_final = pd.concat([tabela_inmet, tabela_inpe_5221, tabela_inpe_5316])

def plot_line(series, *args, **kwargs):
    start = series[series.index > '2021-01-01'].fillna(0).values
    end = series[series.index < '2021-01-01'].fillna(0).values
    le = len(end)
    ls = len(start)
    vals = list(start) + ([0]*(12-le-ls)) + list(end)
    plt.plot(np.arange(len(vals)), vals, *args, **kwargs)

#CONSIDERANDO APENAS PIRANOMETRO (SEM CETESB)
rad = pard.piranometro.radiacao_hora()['Radiacao (W/m2)'].resample('1M').sum()/(1000*30)
t_amb = pard.dados.resample("1M", on="Time")['TEMP(Temperatura do Ar) - °C'].mean()

plt.figure(figsize=(0.82*21, 0.82*7))
ax = sns.barplot(data=tabela_final, x='meses', y='valores', hue='fonte')

plot_line(rad, color=p[3], label="Irradiação Piranômetro")


constante_conversao = 5
def inverse(x):
    return x/constante_conversao

def forward(x):
    return x * constante_conversao

secay = ax.secondary_yaxis('right', functions=(forward, inverse))
secay.set_ylabel('Temp. Ambiente (°C)')
secay.tick_params(right=False)

plot_line(t_amb.map(inverse), '--', color=p[4], label="Temp. Ambiente")

plt.title ("Evolução mensal da irradiação solar global horizontal média diária em Santos - SP")
plt.xlabel ("")
plt.ylabel ("Irradiação")
plt.tick_params(bottom=False, labelbottom=False, axis='both', which='both')
ax.legend().set_visible(False)

x = tabela_final.pivot('meses','fonte')
x.columns = x.columns.droplevel()
x = x.loc[meses].transpose()
def makeDf(x, idx):
    end = x[x.index < '2021-01-01']
    start = x[x.index > '2021-01-01']
    le = len(end)
    ls = len(start)
    vals = list(start.fillna(0).values) + ([0]*(12-le-ls)) + list(end.fillna(0).values)
    vals.append(np.mean(vals))
    return pd.DataFrame([vals], columns=meses, index=[idx])

x = x.append(makeDf(rad, 'Irradiação Piranômetro (Wh/m².dia)'))
x = x.append(makeDf(t_amb, 'Temp. Ambiente (°C)'))

colors = [p[0], p[1], p[2], p[3], p[4]]

tbl = plt.table(
    cellText=np.round(x.values, 2), 
    colLabels=x.columns,
    rowLabels=x.index,
    rowColours =colors,
    bbox=[0.04, -0.55, 0.92, 0.5],
    cellLoc = 'center', rowLoc = 'center',
    loc='bottom', colWidths=[0.075] * 13)
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
plt.tight_layout()
plt.savefig('dados históricos_insolação/evolucao_irradiacao' + EXT, bbox_inches='tight')
#plt.legend()
plt.show()
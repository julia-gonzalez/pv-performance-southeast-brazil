# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 16:45:28 2020

@author: User
"""

import seaborn as sns
import matplotlib.pyplot as plt
import parametros_desempenho as pard
import pandas as pd
from datetime import datetime
import os
import piranometro
import numpy as np
import pymannkendall
    
def _legenda_equacao_linear(p):
    x = p.get_lines()[0].get_xdata()
    y = p.get_lines()[0].get_ydata()
    m = (y[-1] - y[0])/(x[-1] - x[0])
    n = y[0] - m * x[0]
    p.get_lines()[0].set_label("$f(x) = %0.2fx %+0.2f$"  % (m,n))

# def _pega_periodo(df)
#     return df[(df.index.hour >= 8) & (df.index.hour <= 16)]

rad_cetesb_piranometro = piranometro.combinar_cetesb()

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"], index_col=0)

NOCT = 45
dados["T_mod_estimado"] = dados['Temperature(C)'] + dados['Radiacao (W/m2)'] * (NOCT-20)/800
dados["DeltaTempEstimado"] = dados['T_mod_estimado'] - dados['TEMP(Temperatura do Ar) - °C']

hoje = datetime.today()
PASTA = "Gráficos/%s - Gráficos %s/Parâmetros de desempenho/" % (hoje.strftime('%Y%m%d'), hoje.strftime('%d.%m.%Y'))

if not os.path.isdir(PASTA):
    os.mkdir(PASTA)


from config_graficos import EXT, FIGSIZE, ENGLISH, SHOW_TITLE, SHOW_LEGEND, FIGSIZE_HALF, FIGSIZE_SM

PERIODOS = {
        "Ano":     ("2020-10-01", "2021-10-01"),
        "Chuvoso": ("2020-10-01", "2021-04-01"),
        "Seco":    ("2021-04-01", "2021-10-01"),
    }
BINS=100

def extrai_periodo(p, s):
    (comeco, fim) = p
    return s[(s.index >= comeco) & (s.index < fim)]

legenda = 'Legenda' if not ENGLISH else "Legend"


for (nome, _periodo) in PERIODOS.items():
    periodo = lambda s: extrai_periodo(_periodo, s)
   
    
    #Desempenho a nivel de sistema
    plt.figure(figsize=FIGSIZE_HALF)
    wo = periodo(pard.Y_r_h) > 0
    x=periodo(pard.Y_r_h)[wo]
    y=periodo(pard.Y_f_h)[wo]
    sns.histplot(y=y, x=x, bins=BINS)
    p = sns.regplot(y=y, x=x, scatter = False, color = "green")
    
    if SHOW_TITLE:
        plt.title ("PR por Temperatura Ambiente")
    plt.xlabel ("$Y_r$ (h)")
    plt.ylabel ("$Y_f$ (h)")
    
    _legenda_equacao_linear(p)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PASTA + "Desempenho a nivel de sistema_"+nome+EXT)
    plt.show()
    
    #P_R, temp mod
    temp = dados['Temperature(C)'].rename('Temp').reset_index(drop=True)
    temp_est = dados['T_mod_estimado'].rename('Temp').reset_index(drop=True)
    temp_d = dados['Temperature(C)'].resample('1D').mean().rename('Temp').reset_index(drop=True)
    temp_est_d = dados['T_mod_estimado'].resample('1D').mean().rename('Temp').reset_index(drop=True)
    
    pr_temp = (pd.DataFrame([periodo(pard.P_R_d).rename('PR').reset_index(drop=True), temp_d])).T.replace([np.inf, -np.inf], np.nan).dropna()
    pr_temp = pr_temp[(pr_temp.PR > 0) & (pr_temp.PR <= 250)]
    plt.figure(figsize=FIGSIZE_HALF)
    sns.scatterplot(data=pr_temp, y='PR', x='Temp')
    # p = sns.regplot(data=pr_temp, y='PR', x='Temp', scatter = False, color = "green")
    
    if SHOW_TITLE:
        plt.title ("PR por Temperatura Modulo")
    plt.xlabel ("$T_\mathit{mod}$ (°C)")
    plt.ylabel ("$PR$ (%)")
    
    # _legenda_equacao_linear(p)
    # plt.legend()
    # plt.ylim(25,250)
    # plt.xlim(15,55)
    plt.tight_layout()
    plt.savefig(PASTA + "PR por Temperatura Modulo_"+nome+EXT)
    plt.show()
    
    ##
    pr_temp = (pd.DataFrame([periodo(pard.P_R_d).rename('PR').reset_index(drop=True), temp_est_d])).T.replace([np.inf, -np.inf], np.nan).dropna()
    pr_temp = pr_temp[(pr_temp.PR > 0) & (pr_temp.PR <= 250)]
    plt.figure(figsize=FIGSIZE_HALF)
    sns.scatterplot(data=pr_temp, y='PR', x='Temp')
    # p = sns.regplot(data=pr_temp, y='PR', x='Temp', scatter = False, color = "green")
    
    if SHOW_TITLE:
        plt.title ("PR por Temperatura Modulo")
    plt.xlabel ("$T_\mathit{modEstimado}$ (°C)")
    plt.ylabel ("$PR$ (%)")
    
    # _legenda_equacao_linear(p)
    # plt.legend()
    # plt.ylim(25,250)
    # plt.xlim(15,55)
    plt.tight_layout()
    plt.savefig(PASTA + "PR por Temperatura Modulo Estimado_"+nome+EXT)
    plt.show()
    
    
    # Temperatura do módulo FV
    plt.figure(figsize=FIGSIZE_HALF)
    diferenca_temp = periodo(dados['Temperature(C)'] - dados['TEMP(Temperatura do Ar) - °C'])
    sns.histplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), bins=BINS)
    p = sns.regplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), scatter = False, color = "green")
    if SHOW_TITLE:
        plt.title('Temperatura do módulo FV')
    plt.ylabel('$T_{mod} - T_{amb}$ (°C)')
    plt.xlabel('$Y_r$ (h)')
    plt.ylim(-5,20)
    _legenda_equacao_linear(p)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PASTA + "Temperatura do módulo FV_"+nome+EXT)
    plt.show()
    
    # Temperatura estimada do módulo FV
    plt.figure(figsize=FIGSIZE_HALF)
    diferenca_temp = periodo(dados['T_mod_estimado'] - dados['TEMP(Temperatura do Ar) - °C'])
    sns.histplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), bins=BINS)
    p = sns.regplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), scatter = False, color = "green")
    if SHOW_TITLE:
        plt.title('Temperatura do módulo FV')
    plt.ylabel('$T_{modEstimado} - T_{amb}$ (°C)')
    plt.xlabel('$Y_r$ (h)')
    plt.ylim(-10,60)
    _legenda_equacao_linear(p)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PASTA + "Temperatura estimada do módulo FV_"+nome+EXT)
    plt.show()
    
    
    #Resiliência da tensão da rede na potência ativa: VAC versus Yf
    plt.figure(figsize=FIGSIZE_HALF)
    x=periodo(pard.Y_f_h)
    vac = periodo(dados['Ua(V)'])
    sns.histplot(y=vac, x=x, bins=BINS)
    p = sns.regplot(y=vac, x=x, scatter = False, color = "green")
    if SHOW_TITLE:
        plt.title('Resiliência da tensão da rede na potência ativa')
    plt.ylabel('$V_{AC}$ (V)')
    plt.xlabel('$Y_f$ (h)')
    _legenda_equacao_linear(p)
    plt.ylim(215,225)
    plt.xlim(0,1)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PASTA + "VAC versus Yf_"+nome+EXT)
    plt.show()
    
    #Desempenho a nivel de arranjo
    plt.figure(figsize=FIGSIZE_HALF)
    x=periodo(pard.Y_r_h)
    y=periodo(pard.Y_A_h)
    sns.histplot(y=y, x=x, bins=BINS)
    p = sns.regplot(y=y, x=x, scatter = False, color = "green")
    
    if SHOW_TITLE:
        plt.title ("PR por Temperatura Ambiente")
    plt.ylabel ("$Y_A$ (h)")
    plt.xlabel ("$Y_r$ (h)")
    
    _legenda_equacao_linear(p)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PASTA + "Desempenho a nivel de arranjo_"+nome+EXT)
    plt.show()
    
    #P_R_A, temp mod
    pr_temp = pd.DataFrame([periodo(pard.PR_A_d).rename('PR').reset_index(drop=True), temp_d]).T.replace([np.inf, -np.inf], np.nan).dropna()
    pr_temp = pr_temp[(pr_temp.PR > 0) & (pr_temp.PR <= 250)]
    plt.figure(figsize=FIGSIZE_HALF)
    sns.scatterplot(data=pr_temp, y='PR', x='Temp')
    # p = sns.regplot(data=pr_temp, y='PR', x='Temp', scatter = False, color = "green")
    
    if SHOW_TITLE:
        plt.title ("PR por Temperatura Ambiente")
    plt.xlabel ("$T_\mathit{mod}$ (°C)")
    plt.ylabel ("$PR_A$ (%)")
    
    # _legenda_equacao_linear(p)
    # plt.legend()
    # plt.ylim(0,200)
    # plt.xlim(15,55)
    plt.tight_layout()
    plt.savefig(PASTA + "PR_A por Temperatura Modulo_"+nome+EXT)
    plt.show()
    
    #P_R_A, temp mod_estimada
    pr_temp = pd.DataFrame([periodo(pard.PR_A_d).rename('PR').reset_index(drop=True), temp_est_d]).T.replace([np.inf, -np.inf], np.nan).dropna()
    pr_temp = pr_temp[(pr_temp.PR > 0) & (pr_temp.PR <= 250)]
    plt.figure(figsize=FIGSIZE_HALF)
    sns.scatterplot(data=pr_temp, y='PR', x='Temp')
    # p = sns.regplot(data=pr_temp, y='PR', x='Temp', scatter = False, color = "green")
    
    plt.xlabel ("$T_{modEstimado}$ (°C)")
    plt.ylabel ("$PR_A$ (%)")
    
    # _legenda_equacao_linear(p)
    # plt.legend()
    # plt.ylim(0,200)
    # plt.xlim(15,55)
    plt.tight_layout()
    plt.savefig(PASTA + "PR_A por Temperatura Modulo Estimado_"+nome+EXT)
    plt.show()
    
    
    
    # Tensão do arranjo: VDCversusTmod
    plt.figure(figsize=FIGSIZE_HALF)
    sns.histplot(data=periodo(dados), y='V MPPT 1(V)', x='Temperature(C)', bins=BINS)
    p = sns.regplot(data=periodo(dados), y='V MPPT 1(V)', x='Temperature(C)', scatter = False, color = "green")
    if SHOW_TITLE:
        plt.title('Tensão do arranjo')
    plt.xlabel('$T_{mod}$ (°C)')
    plt.ylabel('$V_{DC}$ (V)')
    _legenda_equacao_linear(p)
    plt.legend()
    plt.ylim(120,160)
    plt.xlim(11,55)
    plt.tight_layout()
    plt.savefig(PASTA + "VDC versus Tmod_"+nome+EXT)
    plt.show()
    
    # Tensão do arranjo: VDCversusTmodEstimado
    plt.figure(figsize=FIGSIZE_HALF)
    sns.histplot(data=periodo(dados), y='V MPPT 1(V)', x='T_mod_estimado', bins=BINS)
    p = sns.regplot(data=periodo(dados), y='V MPPT 1(V)', x='T_mod_estimado', scatter = False, color = "green")
    if SHOW_TITLE:
        plt.title('Tensão do arranjo')
    plt.xlabel('$T_{modEstimado}$ (°C)')
    plt.ylabel('$V_{DC}$ (V)')
    _legenda_equacao_linear(p)
    plt.legend()
    plt.ylim(120,160)
    plt.xlim(11,55)
    plt.tight_layout()
    plt.savefig(PASTA + "VDC versus TmodEst_"+nome+EXT)
    plt.show()


#E_CA x Rad
e_ac = pard.E_ac_h
sem_outliers = (e_ac > -0.5) & (e_ac < 4)
e_ac = e_ac[sem_outliers]
cor = rad_cetesb_piranometro.reindex(e_ac.index).Fonte
plt.figure(figsize=FIGSIZE)
sns.scatterplot(y=e_ac, x=pard.rad_h.reindex(e_ac.index), hue=cor)
sns.regplot(y=e_ac, x=pard.rad_h.reindex(e_ac.index), scatter = False, color = "green")

if SHOW_TITLE:
    plt.title ("Relação entre radiação e energia produzida")
plt.xlabel ("Radiação solar global (W/m²)")
plt.ylabel ("Energia produzida em CA (kWh)")

plt.tight_layout()
plt.savefig(PASTA + "E_CA x Rad"+EXT)
plt.show()

#Y_R, Y_F, perdas totais: atenção que o Y_r não aparece por ser valores muito pequenos. Ver com o Fernando se fiz algo errado!
fig, ax = plt.subplots(figsize=FIGSIZE_SM)
perdas = pd.melt(pd.DataFrame(data=[
    pard.Y_r_d.resample("1M").mean().rename('$Y_r$'), 
    pard.Y_f_d.resample("1M").mean().rename("$Y_f$"), 
    pard.L_T_d.resample("1M").mean().rename('$L_S$')*-1
    ]).T.reset_index(), id_vars='Time').rename({'variable': legenda}, axis=1)

sns.barplot(data=perdas, x='Time', y='value', hue=legenda)

ax.set_xticklabels(labels=perdas.Time.dt.strftime("%m/%y").unique())
if SHOW_TITLE:
    plt.title ("$Y_R$, $Y_F$ e Perdas Totais")
plt.xlabel ("Tempo"  if not ENGLISH else "Month")
plt.ylabel ("Horas de Sol"  if not ENGLISH else "$\mathit{kWh}$/$\mathit{kWp}\cdot\mathit{day}$")
if not SHOW_LEGEND:
    plt.legend([],[], frameon=False)
plt.xticks(rotation=45)
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig(PASTA + "YR, YF e Perdas Totais"+EXT)
plt.show()

#P_R, F_C, N_SYS: atenção que o Y_r deve estar com erro mesmo, pois afetou o PR
fig, ax = plt.subplots(figsize=FIGSIZE_SM)
desempenho = pd.melt(pd.DataFrame(data=[
    pard.P_R_m.rename('$PR$')/5, 
    pard.CF_m.rename("$CF$"), 
    pard.N_SYS_m.rename('$\eta_{SYS}$')
    ]).T.reset_index(), id_vars='Time').rename({'variable': legenda}, axis=1)

sns.barplot(data=desempenho, x='Time', y='value', hue=legenda)

ax.set_xticklabels(labels=perdas.Time.dt.strftime("%m/%y").unique())
if SHOW_TITLE:
    plt.title ("PR, CF e Eficiência do Sistema")
plt.xlabel ("Tempo" if not ENGLISH else "Month")
plt.ylabel ("% $CF$,$\eta_{SYS}$")
plt.xticks(rotation=45)

if not SHOW_LEGEND:
    ax.legend([],[], frameon=False)

plt.legend(loc='upper left', bbox_to_anchor=(1.01, -0.01))
plt.ylim(0,20)
ax2 = ax.twinx()
ax2.legend([],[], frameon=False)
ax2.set_ylim([0,100])
ax2.set_yticks(np.arange(9)*2.5*5)
ax2.grid(False)
ax2.set_ylabel("% PR")
ax.tick_params(axis=u'both', which=u'both',length=0)
ax2.tick_params(axis=u'both', which=u'both',length=0)
sns.despine()
plt.tight_layout()
plt.savefig(PASTA + "PR, CF e Eficiência do Sistema"+EXT)
plt.show()

#SWC
fig, ax = plt.subplots(figsize=FIGSIZE)
scale = 4
desempenho = pd.melt(pd.DataFrame(data=[
    pard.P_R_m.rename('$PR$'), 
    pard.CF_m.rename("$CF$") * scale, 
    ]).T.reset_index(), id_vars='Time').rename({'variable': legenda}, axis=1)

sns.barplot(data=desempenho, x='Time', y='value', hue=legenda, palette=["C3", "C4"])

ax.set_xticklabels(labels=perdas.Time.dt.strftime("%m/%y").unique())
ax.set_ylim(0,100)
plt.xlabel ("Tempo" if not ENGLISH else "Time")
plt.ylabel ("$PR$")
plt.xticks(rotation=45)
ax2 = ax.twinx()

# Ensure ticks occur at the same positions, then modify labels
ax2.set_ylim(ax.get_ylim())
ax2.set_yticklabels((ax.get_yticks()/scale).astype(int))
ax2.set_ylabel('% $CF$')
ax2.grid(b=None)
ax.set_yticklabels((ax.get_yticks()/100).round(1))
if not SHOW_LEGEND:
    ax.legend([],[], frameon=False)

plt.tight_layout()
plt.savefig(PASTA + "SWC - PR, CF e Eficiência do Sistema"+EXT)
plt.show()

#P_R, temp amb: o PR continua zuando tudo
pr_temp = pd.DataFrame([pard.P_R_d.rename('PR'), dados['TEMP(Temperatura do Ar) - °C'].resample("1D").mean().rename('Temp')]).T.dropna()
pr_temp = pr_temp[(pr_temp.PR > 0) & (pr_temp.PR <= 250)]
plt.figure(figsize=FIGSIZE)
sns.scatterplot(data=pr_temp, y='PR', x='Temp')
sns.regplot(data=pr_temp, y='PR', x='Temp', scatter = False, color = "green")

if SHOW_TITLE:
    plt.title ("PR por Temperatura Ambiente")
plt.xlabel ("Temperatura Ambiente (°C)")
plt.ylabel ("PR (%)")

plt.tight_layout()
plt.savefig(PASTA + "PR por Temperatura Ambiente"+EXT)
plt.show()


# Temperatura do módulo FV
plt.figure(figsize=FIGSIZE_HALF)
diferenca_temp = dados['Temperature(C)'] - dados['TEMP(Temperatura do Ar) - °C']
sns.histplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), bins=BINS)
p = sns.regplot(y=diferenca_temp, x=pard.Y_r_h.reindex(diferenca_temp.index), scatter = False, color = "green")
if SHOW_TITLE:
    plt.title('Temperatura do módulo FV')
plt.ylabel('$T_{mod} - T_{amb}$ (°C)')
plt.xlabel('$Y_r$ (h)')
_legenda_equacao_linear(p)
plt.legend()
plt.tight_layout()
plt.savefig(PASTA + "Temperatura do módulo FV"+EXT)
plt.show()

# Temperatura do módulo FV
plt.figure(figsize=FIGSIZE)
outlier_mask = (pard.P_R_d < 200)

x = pard.rad_d[outlier_mask]
y = pard.P_R_d[outlier_mask]

sns.scatterplot(y=y, x=x)
sns.regplot(y=y, x=x, color = "green", scatter=False)
if SHOW_TITLE:
    plt.title('Comparação do $\mathit{PR}$ com Irrandiância')
plt.ylabel('$\mathit{PR}$ (%)')
plt.xlabel('$G_I$ ($Wh/m^2$)')
plt.tight_layout()
plt.savefig(PASTA + "PR por Irrandiância"+EXT)
plt.show()

# CF - Mann Kendal
plt.figure(figsize=FIGSIZE)
roll = pard.CF_d.rolling(7).mean()
mk = pymannkendall.original_test(roll.values)
plt.text(0.05, 0.95, f"$p$-value = {mk.p:.3f}",
         transform=plt.gca().transAxes,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

mint = roll.index.min()
maxt = roll.index.max()
delta = (maxt - mint).days

sns.scatterplot(y=roll, x=roll.index)
pd.Series(
    [mk.intercept, mk.intercept + mk.slope*delta], 
          index=[mint, maxt]).plot(color='C2', label=f"$f(x) = {mk.slope:.3f}x + {mk.intercept:.1f}$")

plt.ylabel('CF (%) - Média móvel dos últimos 7 dias')
plt.xlabel('Tempo')
plt.legend()
plt.tight_layout()
plt.savefig(PASTA + "Mann Kendal DF"+EXT)
plt.show()
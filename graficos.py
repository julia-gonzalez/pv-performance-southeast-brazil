import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, MonthLocator
from datetime import datetime
import os
from config_graficos import FIGSIZE, EXT, FIGSIZE_SM, ENGLISH, SHOW_TITLE, SHOW_LEGEND, FIGSIZE_HALF
import parametros_desempenho as pard
import numpy as np
from scipy import stats


dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])
dados['DeltaTemp'] = dados['Temperature(C)'] - dados['TEMP(Temperatura do Ar) - °C']
dados['RazaoTemp'] = dados['Temperature(C)'] / dados['TEMP(Temperatura do Ar) - °C']
NOCT = 45
dados["T_mod_estimado"] = dados['Temperature(C)'] + dados['Radiacao (W/m2)'] * (NOCT-20)/800
dados["DeltaTempEstimado"] = dados['T_mod_estimado'] - dados['TEMP(Temperatura do Ar) - °C']
hoje = datetime.today()
PASTA = "Gráficos/%s - Gráficos %s/" % (hoje.strftime('%Y%m%d'), hoje.strftime('%d.%m.%Y'))




PERIODOS = {
        "Ano":     ("2020-10-01", "2021-10-01"),
        "Chuvoso": ("2020-10-01", "2021-04-01"),
        "Seco":    ("2021-04-01", "2021-10-01"),
    }
def extrai_periodo(p, s):
    (comeco, fim) = p
    return s[(s.Time >= comeco) & (s.Time < fim)]

myFmt = DateFormatter("%m/%y")
def _line_format(label):
    y = str(label.year)[2:]
    return "%02d/%s" % (label.month, y)

if not os.path.isdir(PASTA):
    os.mkdir(PASTA)


def temp_modfv_ar_tempo(): 
    fig, ax = plt.subplots(figsize=FIGSIZE_SM)
    
    energia_diaria =  dados.resample('7d', on = 'Time')
    mean = energia_diaria.median()
    q1 = energia_diaria.quantile(0.25)
    q3 = energia_diaria.quantile(0.75)
    
    def plot_line(col, color, label):
        sns.lineplot(y=col, x = mean.index, data = mean, label = label)
        plt.fill_between(mean.index, q1[col], q3[col], color=color, alpha=0.2)  
    plot_line('Temperature(C)', "C0", '$T_{mod}$')
    plot_line('TEMP(Temperatura do Ar) - °C', "C1", '$T_{amb}$')
    plot_line('T_mod_estimado', "C2", '$T_{modEstimado}$')

    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_locator(MonthLocator())
    
    if SHOW_TITLE:
        plt.title ("Temperaturas médias diárias do sist FV e do ar ao longo do tempo")
    plt.xlabel ("Tempo" if not ENGLISH else "Time")
    plt.ylabel ("Temperatura (°C)"  if not ENGLISH else "Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend ()
    
    plt.tight_layout()
        
    plt.savefig(PASTA + 'temp_modfv_ar_tempo' + EXT)

def _legenda_equacao_linear(p):
    x = p.get_lines()[0].get_xdata()
    y = p.get_lines()[0].get_ydata()
    m = (y[-1] - y[0])/(x[-1] - x[0])
    n = y[0] - m * x[0]
    p.get_lines()[0].set_label("$f(x) = %0.2fx %+0.2f$"  % (m,n))

def _r2(x,y):
    (x1, y1) = x.dropna().align(y.dropna(), 'inner')
    plt.title("$R^2 = %.2f$" % stats.pearsonr(x1, y1)[0] ** 2)

def temp_modfv_ar_prop():   
    plt.figure(figsize=FIGSIZE_SM)   
  
    sns.scatterplot(y='Temperature(C)', x='TEMP(Temperatura do Ar) - °C', data = dados)
    p = sns.regplot(y='Temperature(C)', x='TEMP(Temperatura do Ar) - °C', data = dados, scatter = False, color = 'green')
    
    if SHOW_TITLE:
        plt.title ("Correlação entre as temperaturas do sist FV e do ar")
    plt.xlabel ("Temperatura do ar (°C)")
    plt.ylabel ("Temperatura do sist FV (°C)")
    
    _legenda_equacao_linear(p)
    plt.legend()
    
    plt.tight_layout()
    
    x1,x2,y1,y2 = plt.axis()
    mx = max(x2, y2)
    plt.axis((15,mx,15,mx))
        
    plt.savefig(PASTA + 'temp_modfv_ar_prop' + EXT)
    
def influencias_temp_modfv_vs_ar():
    plt.figure(figsize=FIGSIZE_SM)   
  
    sns.pairplot(y_vars='DeltaTemp', data = dados, aspect=2)

    if SHOW_TITLE:
        plt.title ("Correlação entre o DeltaTemp e diferentes variáveis")
    
    plt.xlabel("Difference between module and air temperature")
    plt.tight_layout()
        
    plt.savefig(PASTA + 'influencias_temp_modfv_vs_ar' + EXT)
def histograma_delta_temp():
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        x = periodo(dados).DeltaTemp.dropna()
        x.plot.hist(bins=30, weights = 100*np.ones_like(x.index) / len(x.index))
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        
        plt.xlabel("$\Delta T$ (°C)")
        if not ENGLISH:
            plt.ylabel("Porcentagem (%)")
        else:
            plt.ylabel("Frquency (%)")
        plt.xlim(-5,19)
        plt.ylim(0,9)
        plt.tight_layout()
        plt.savefig(PASTA + 'histograma_delta_temp_'+nome+EXT)
        
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        x = periodo(dados).DeltaTempEstimado.dropna()
        x.plot.hist(bins=30, weights = 100*np.ones_like(x.index) / len(x.index))
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas estimada do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        
        plt.xlabel("$\Delta T_{estimado}$ ano (°C)")
        if not ENGLISH:
            plt.ylabel("Porcentagem (%)")
        else:
            plt.ylabel("Frquency (%)")
        # plt.xlim(-5,19)
        plt.ylim(0,9)
        plt.tight_layout()
        plt.savefig(PASTA + 'histograma_delta_temp_estimado_'+nome+EXT)

    
# def temp_ambiente_vs_delta_temp():
#     fig, ax = plt.subplots(figsize=FIGSIZE)
    
#     diarios = dados.resample('1d', on = 'Time').mean()
  
#     sns.scatterplot(y='DeltaTemp', x='TEMP(Temperatura do Ar) - °C', data = diarios)
#     sns.regplot(y='DeltaTemp',  x='TEMP(Temperatura do Ar) - °C', data = diarios, scatter = False, color='green')

#     if SHOW_TITLE:
#         plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
    
#     plt.tight_layout()
#     plt.ylabel("Daily Average $\Delta T$ (°C)")
#     plt.xlabel("Daily Average $T_{amb}$ (°C)")
#     plt.axis('equal')
        
#     plt.savefig(PASTA + 'temp_ambiente_vs_delta_temp' + EXT)

def temp_ambiente_vs_delta_temp_dias_ensolarados():
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        
        diarios = periodo(dados).resample('1d', on = 'Time').max()
        ensolarados = periodo(dados).resample('1d', on = 'Time').sum()
        diarios = diarios[ensolarados['Radiacao (W/m2)'] > 600]
      
        sns.scatterplot(x='DeltaTemp', y='TEMP(Temperatura do Ar) - °C', data = diarios)
        sns.regplot(x='DeltaTemp',  y='TEMP(Temperatura do Ar) - °C', data = diarios, scatter = False, color='green')
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        
        plt.tight_layout()
        if ENGLISH:
            plt.xlabel("Daily Maximum $\Delta T$ (°C)")
            plt.ylabel("Daily Maximum $T_{amb}$ (°C)")
        else:
            plt.xlabel("$\Delta T$ Máximo Diário (°C)")
            plt.ylabel("$T_{amb}$ Máximo Diário (°C)")
        plt.xlim(2,20)
            
        plt.savefig(PASTA + 'temp_ambiente_vs_delta_temp_dias_ensolarados_'+nome+EXT)
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        
        diarios = periodo(dados).resample('1d', on = 'Time').max()
        ensolarados = periodo(dados).resample('1d', on = 'Time').sum()
        diarios = diarios[ensolarados['Radiacao (W/m2)'] > 600]
      
        sns.scatterplot(x='DeltaTempEstimado', y='TEMP(Temperatura do Ar) - °C', data = diarios)
        sns.regplot(x='DeltaTempEstimado',  y='TEMP(Temperatura do Ar) - °C', data = diarios, scatter = False, color='green')
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        
        plt.tight_layout()
        if ENGLISH:
            plt.xlabel("Daily Maximum $\Delta T$ (°C)")
            plt.ylabel("Daily Maximum $T_{amb}$ (°C)")
        else:
            plt.xlabel("$\Delta T_{estimado}$ Máximo Diário (°C)")
            plt.ylabel("$T_{amb}$ Máximo Diário (°C)")
        plt.xlim(2,50)
            
        plt.savefig(PASTA + 'temp_ambiente_vs_delta_temp_estimado_dias_ensolarados_'+nome+EXT)

def delta_temp_vs_radiacao():
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        
        diarios = periodo(dados).resample('1d', on = 'Time')
        x = diarios['DeltaTemp'].max()
        y = diarios['Radiacao (W/m2)'].mean()
        
      
        sns.scatterplot(x=x, y=y)
        p = sns.regplot(x=x,  y=y, scatter = False, color='green')
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        else:
            _r2(x,y)
        
        plt.tight_layout()
        if ENGLISH:
            plt.xlabel("Daily Maximum $\Delta T$ (°C)")
            plt.ylabel("Daily Average Irradiance ($W/m^2$)")
        else:
            plt.xlabel("$\Delta T$ Máximo Diário (°C)")
            plt.ylabel("$G_I$ Média Diária($W/m^2$)")
        plt.xlim(2,20)
        _legenda_equacao_linear(p)
        plt.legend(loc="upper left")
        plt.savefig(PASTA + 'delta_temp_vs_radiacao_'+nome+EXT)
    for (nome, _periodo) in PERIODOS.items():
        periodo = lambda s: extrai_periodo(_periodo, s)
        fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
        
        diarios = periodo(dados).resample('1d', on = 'Time')
        x = diarios['DeltaTempEstimado'].max()
        y = diarios['Radiacao (W/m2)'].mean()
        
      
        sns.scatterplot(x=x, y=y)
        p = sns.regplot(x=x,  y=y, scatter = False, color='green')
    
        if SHOW_TITLE:
            plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
        else:
            _r2(x,y)
        
        plt.tight_layout()
        if ENGLISH:
            plt.xlabel("Daily Maximum $\Delta T_{estimado}$ (°C)")
            plt.ylabel("Daily Average Irradiance ($W/m^2$)")
        else:
            plt.xlabel("$\Delta T_{estimado}$ Máximo Diário (°C)")
            plt.ylabel("$G_I$ Média Diária($W/m^2$)")
        plt.xlim(2,50)
        _legenda_equacao_linear(p)
        plt.legend(loc="upper left")
        plt.savefig(PASTA + 'delta_temp_estimado_vs_radiacao_'+nome+EXT)

def temp_ambiente_vs_delta_temp():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    
    diarios = dados.resample('1d', on = 'Time').mean()
  
    sns.scatterplot(y='DeltaTemp', x='TEMP(Temperatura do Ar) - °C', data = diarios)
    sns.regplot(y='DeltaTemp',  x='TEMP(Temperatura do Ar) - °C', data = diarios, scatter = False, color='green')

    if SHOW_TITLE:
        plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
    
    plt.tight_layout()
    plt.ylabel("$\Delta$ between module and air temperature")
    plt.xlabel("Air temperature (°C)")
    plt.axis('equal')
        
    plt.savefig(PASTA + 'temp_ambiente_vs_delta_temp' + EXT)

def energiatotalprod_tempo():   
    plt.figure(figsize=FIGSIZE_SM)   
  
    fig, ax = plt.subplots(figsize=FIGSIZE_SM)
    
    sns.lineplot(y='ETotal(kWh)', x = 'Time', data = dados)
 
    ax.xaxis.set_major_formatter(myFmt)
    
    if SHOW_TITLE:
        plt.title ("Energia produzida acumulada ao longo do tempo")
    plt.xlabel ("Tempo")
    plt.ylabel ("Energia total produzida (kWh)")

    plt.tight_layout()
        
    plt.savefig(PASTA + 'energiatotalprod_tempo' + EXT)
    
def energia_tempo():   
    plt.figure(figsize=FIGSIZE)   
  
    fig, ax = plt.subplots(figsize=FIGSIZE_SM)
    
    energia_diaria =  dados.resample('1d', on = 'Time').max()
    
    #Decidimos utilizar o valor máximo diário do Eday (kWh), por se tratar de um acumulado ao longo de cada dia
    
    sns.lineplot(y= energia_diaria['Generation Today(kWh)'], x = energia_diaria.index)
     
    ax.xaxis.set_major_formatter(myFmt)
 
    if SHOW_TITLE:
        plt.title ("Energia diária produzida ao longo do tempo")
    plt.xlabel ("Tempo")
    plt.ylabel ("Energia (kWh)")
    #plt.legend ()
    
    plt.tight_layout()
        
    plt.savefig(PASTA + 'energia_tempo' + EXT)
    
def potencia_umidade():   
    plt.figure(figsize=FIGSIZE)   
  
    sns.scatterplot(y='Power(W)', x='UR(Umidade Relativa do Ar) - %', data = dados)
    sns.regplot(y='Power(W)', x='UR(Umidade Relativa do Ar) - %', data = dados, scatter = False, color = 'green')
  
    if SHOW_TITLE:
        plt.title ("Correlação entre UR do ar e potência instantânea")
    plt.xlabel ("Umidade relativa do ar (%)")
    plt.ylabel ("Potência instantânea produzida em CA (W)")
    
    plt.tight_layout()
        
    plt.savefig(PASTA + 'potencia_umidade' + EXT)

#OBS: pesquisar método estatístico utilizado pelo Regplot pra colocar na dissertação! Provavelmente é o de mínimos quadrados, mas pode ser trocado.

def vvento_temp_modfv():
    plt.figure(figsize=FIGSIZE)   
  
    sns.scatterplot(y='Temperature(C)', x='Vel_Vento', data = dados)
    sns.regplot(y='Temperature(C)', x='Vel_Vento', data = dados, scatter = False, color = 'green')
  
    if SHOW_TITLE:
        plt.title ("Correlação entre velocidade do vento e temperatura do sistema FV")
    plt.xlabel ("Velocidade do Vento (m/s)")
    plt.ylabel ("Temperatura do sistema FV (°C)")
    
    plt.tight_layout()
        
    plt.savefig(PASTA + 'vvento_temp_modfv' + EXT)
    
#OBS: não ficou um gráfico bom, provavelmente pq as medições de vvento não são confiáveis     

def potencia_sombreamento():    
    plt.figure(figsize=FIGSIZE)  
  
    def sombreamento(x, label): 
        # sns.scatterplot(y='Power(W)', x= x, data = dados, label=label)
        sns.regplot(y='Power(W)', x=x, data = dados, scatter = False, label=label)
      
    sombreamento ('MP10(Partículas Inaláveis) - µg/m3', 'Partículas Inaláveis')
    sombreamento ('MP2.5(Partículas Inaláveis Finas) - µg/m3', 'Partículas Inaláveis Finas')
    sombreamento ('O3(Ozônio) - µg/m3', 'Ozônio')
    plt.xscale("log")
      
    if SHOW_TITLE:
        plt.title ("Correlação entre sombreamento e potência instantânea")
    plt.xlabel ("Concentração ($\mu g/m^3$)")
    plt.ylabel ("Potência instantânea produzida em CA (W)")
    
    plt.legend()
    plt.tight_layout()
        
    plt.savefig(PASTA + 'potencia_sombreamento' + EXT)

def potencia_radiacao():
    pot_rad = 'Gráficos potência radiação/'
    if not os.path.isdir(PASTA + pot_rad):
        os.mkdir(PASTA + pot_rad)
    idx = pd.DatetimeIndex(dados.Time)
    for date, df in dados.groupby([idx.month, idx.year]):
        plt.figure(figsize=FIGSIZE_SM)
        sns.scatterplot(data=df, y='Power(W)', x='RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro', hue="Fonte")
        sns.regplot(data=df, y='Power(W)', x='RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro', scatter=False, color='green')
        
        if SHOW_TITLE:
            plt.title ("Correlação entre radiação e potência instantânea %02d/%d" % date)
        plt.ylabel ("Potência instantânea produzida em CA (W)")
        plt.xlabel ("Radiação Solar Global ($W/m^2$)")
        
        plt.legend(loc="upper left")
        plt.tight_layout()
        
        plt.savefig(PASTA + pot_rad + ('%02d-%d' % date) + EXT)
        plt.show()

def energia_diaria_X_umidade_media_santos():
    plt.figure(figsize=FIGSIZE_SM)   
    
    resampled = dados.resample('1d', on='Time')
    
    x = resampled.mean()['UR(Umidade Relativa do Ar) - % - Guilherme Alvaro']
    y = resampled.max()['Generation Today(kWh)']
  
    sns.scatterplot(y=y, x=x)
    sns.regplot(y=y, x=x, scatter = False, color = 'green')
  
    if SHOW_TITLE:
        plt.title ("Correlação entre UR do ar e energia gerada")
    plt.xlabel ("Média diária de UR do ar (%) - Santos (GA)")
    plt.ylabel ("Energia total gerada no dia (KWh)")
    
    plt.tight_layout()
    
    plt.savefig(PASTA + 'energia_umidade_ga' + EXT)
    
def energia_diaria_X_umidade_media_pp():
    plt.figure(figsize=FIGSIZE_SM)   
    
    resampled = dados.resample('1d', on='Time')
    
    x = resampled.mean()['UR(Umidade Relativa do Ar) - %']
    y = resampled.max()['Generation Today(kWh)']
  
    sns.scatterplot(y=y, x=x)
    sns.regplot(y=y, x=x, scatter = False, color = 'green')
  
    if SHOW_TITLE:
        plt.title ("Correlação entre UR do ar e energia gerada")
    plt.xlabel ("Média diária de UR do ar (%) - Santos (PP)")
    plt.ylabel ("Energia total gerada no dia (KWh)")
    
    plt.tight_layout()
    
    plt.savefig(PASTA + 'energia_umidade_pp' + EXT)
    

def proporcao_temperatura_X_vvento():
    plt.figure(figsize=FIGSIZE)   
    
    proporcao_temperatura = dados['Temperature(C)']/dados['TEMP(Temperatura do Ar) - °C']
    x = dados['Vel_Vento']
    mask = x > 0
    x = x[mask]
    proporcao_temperatura = proporcao_temperatura[mask]
  
    sns.scatterplot(y=proporcao_temperatura, x=x)
    sns.regplot(y=proporcao_temperatura, x=x, scatter = False, color = 'green')
  
    if SHOW_TITLE:
        plt.title ("Correlação entre Velocidade do Vento e Temperatura")
    plt.xlabel ("Velocidade do Vento (m/s) - Estação UNIFESP")
    plt.ylabel ("$T_\mathit{mod} / T_\mathit{amb}$")
    
    plt.tight_layout()
    
    plt.savefig(PASTA + 'proporcao_temperatura_vvento' + EXT)

def radiacao_ao_longo_do_tempo():
    plt.figure(figsize=FIGSIZE)   
    #rad ao longo do tempo(dia)
    diarios = dados.resample('1d', on='Time').sum()
    pir = dados.loc[dados.Fonte == 'Piranômetro'].resample('1d', on='Time').sum()
    sns.lineplot(data=diarios, x=diarios.index, y='RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro', label="CETESB")
    sns.lineplot(data=pir, x=pir.index, y='Radiacao (W/m2)', alpha=0.75, label="Piranômetro")
    plt.gca().xaxis.set_major_formatter(myFmt)
    
    if SHOW_TITLE:
        plt.title ("Radiação ao longo do tempo")
    plt.xlabel ("Tempo (dia)")
    plt.ylabel ("Radiação solar global (W/m²)")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "rad ao longo do tempo(dia)"+EXT)
    
def radiacao_cetesb_vs_piranometro():
    plt.figure(figsize=FIGSIZE)   
    #rad ao longo do tempo(dia)
    pir = dados.loc[dados.Fonte == 'Piranômetro'].resample('1d', on='Time').sum()
    sns.scatterplot(data=pir, y='Radiacao (W/m2)', x='RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro')
    sns.regplot(data=pir, y='Radiacao (W/m2)', x='RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro', scatter=False, color="green")
    
    x1,x2,y1,y2 = plt.axis()
    mx = max(x2, y2)
    plt.axis((0,mx,0,mx))
    
    if SHOW_TITLE:
        plt.title ("Radiação segundo diferentes fontes")
    plt.xlabel ("CETESB (W/m²)")
    plt.ylabel ("Piranômetro (W/m²)")
    
    plt.tight_layout()
    plt.savefig(PASTA + "rad_cetesb_vs_piranometro"+EXT)
    
def guilherme_alvaro_vs_pp():
    plt.figure(figsize=FIGSIZE)
    
    sns.scatterplot(data=dados, x="UR(Umidade Relativa do Ar) - % - Guilherme Alvaro", y="UR(Umidade Relativa do Ar) - %")
    sns.regplot(data=dados, x="UR(Umidade Relativa do Ar) - % - Guilherme Alvaro", y="UR(Umidade Relativa do Ar) - %", scatter=False, color="green")
    
    if SHOW_TITLE:
        plt.title ("Comparação entre estações da CETESB")
    plt.xlabel ("UR (%) - GA")
    plt.ylabel ("UR (%) - PP")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "ga_vs_pp_ur"+EXT)
    
    plt.figure(figsize=FIGSIZE)
    
    sns.scatterplot(data=dados, x="TEMP(Temperatura do Ar) - °C - Guilherme Alvaro", y="TEMP(Temperatura do Ar) - °C")
    sns.regplot(data=dados, x="TEMP(Temperatura do Ar) - °C - Guilherme Alvaro", y="TEMP(Temperatura do Ar) - °C", scatter=False, color="green")
    
    if SHOW_TITLE:
        plt.title ("Comparação entre estações da CETESB")
    plt.xlabel ("Temperatura (°C) - GA")
    plt.ylabel ("Temperatura (°C) - PP")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "ga_vs_pp_temp"+EXT)

def comparacao_solergo_radiacao():
    rad_piranometro = pard.rad_m
    
    rad_solergo = [114.321, 125.227, 144.917, 144.681, 144.94, 134.225, 123.245, 111.536, 99.054, 102.9, 119.51, 104.544]
    
    tabela_rad_total = pd.DataFrame()
    tabela_rad_total["Piranômetro" if not ENGLISH else "Pyranometer"] = rad_piranometro/1000
    tabela_rad_total["Solergo"] = rad_solergo[0:len(rad_piranometro)]
    
    ax = tabela_rad_total.plot(kind="bar", rot=0, figsize=FIGSIZE_SM, color=["C2", "C6"])
    ax.set_xticklabels(map(_line_format, tabela_rad_total.index))
    if SHOW_TITLE:
        plt.title("Comparação entre irradiação projetada e real")
    plt.xlabel("Tempo" if not ENGLISH else "Month")
    plt.ylabel("$H_I$ ($kWh/m^2$)")
    # plt.ylim(0,180)
    if not SHOW_LEGEND:
        plt.legend([],[], frameon=False)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PASTA + "comparacao_solergo_radiacao"+EXT)

def comparacao_solergo_energia():
    energia_piranometro = pard.E_ac_m
    
    energia_solergo = [123.882, 135.699, 157.036, 156.781, 157.062, 145.45, 133.552, 120.864, 107.338, 111.506, 129.505, 113.287]
    
    tabela_energia_total = pd.DataFrame()
    tabela_energia_total["PHB"] = energia_piranometro
    tabela_energia_total["Solergo"] = energia_solergo[0:len(energia_piranometro)]
    
    ax = tabela_energia_total.plot(kind="bar", rot=0, figsize=FIGSIZE_SM, color=["C2", "C6"])
    ax.set_xticklabels(map(_line_format, tabela_energia_total.index))
    if SHOW_TITLE:
        plt.title("Comparação entre energia projetada e real")
    plt.xlabel("Tempo" if not ENGLISH else "Month")
    plt.ylabel("$E_\mathit{AC}$ ($kWh$)" if not ENGLISH else "Energy ($kWh$)")
    if not SHOW_LEGEND:
        plt.legend([],[], frameon=False)
    # plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(PASTA + "comparacao_solergo_energia"+EXT)

def irradiancia_vs_potencia():
    plt.figure(figsize=FIGSIZE)
    
    sns.scatterplot(data=dados, x="Radiacao (W/m2)", y="Power(W)")
    p = sns.regplot(data=dados, x="Radiacao (W/m2)", y="Power(W)", scatter=False, color="green")
    
    if SHOW_TITLE:
        plt.title ("Comparação entre potência e radiação")
    plt.xlabel ("$G_I$ ($W/m^2$)")
    plt.ylabel ("$P_{AC}$ ($W$)")
    _legenda_equacao_linear(p)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "irradiancia_vs_potencia"+EXT)
def razao_temp_vs_irradiancia():
    plt.figure(figsize=FIGSIZE)
    remove_outlier = dados[dados['Radiacao (W/m2)'] > 0]
    remove_outlier = dados[(dados.Time.dt.hour >= 8) & (dados.Time.dt.hour <= 16)]
    
    sns.scatterplot(data=remove_outlier, y="Radiacao (W/m2)", x="RazaoTemp")
    sns.regplot(data=remove_outlier, y="Radiacao (W/m2)", x="RazaoTemp", scatter=False, color="green")
    plt.ylim((-100, dados['Radiacao (W/m2)'].max()+100))
    
    if SHOW_TITLE:
        plt.title ("Comparação entre irradiâcncia e razão de temperatura (horária)")
    plt.ylabel ("$G_I$ ($W/m^2$)")
    plt.xlabel ("$T_{mod} / T_{amb}$")
    # plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "razao_temp_vs_irradiancia_hora"+EXT)
    ######
    plt.figure(figsize=FIGSIZE)
    diario = remove_outlier.resample('1D', on='Time').mean()
    
    sns.scatterplot(data=diario, y="Radiacao (W/m2)", x="RazaoTemp")
    sns.regplot(data=diario, y="Radiacao (W/m2)", x="RazaoTemp", scatter=False, color="green")
    plt.ylim((-100, dados['Radiacao (W/m2)'].max()+100))
    
    if SHOW_TITLE:
        plt.title ("Comparação entre irradiâcncia e razão de temperatura (diária)")
    plt.ylabel ("$G_I$ ($W/m^2$)")
    plt.xlabel ("$T_{mod} / T_{amb}$")
    # plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "razao_temp_vs_irradiancia_dia"+EXT)

def material_particulado():
    plt.figure(figsize=FIGSIZE_SM)
    mp10 = pd.DataFrame({
        "value": dados['MP10(Partículas Inaláveis) - µg/m3'],
        "Medida": 'MP10',
        "month": dados.Time.dt.strftime('%m/%Y')
        })
    mp25 = pd.DataFrame({
        "value": dados['MP2.5(Partículas Inaláveis Finas) - µg/m3'],
        "Medida": 'MP2.5',
        "month": dados.Time.dt.strftime('%m/%Y')
        })
    boxes = pd.concat([mp10, mp25])
    sns.boxplot(data=boxes, y='value', x='month', hue='Medida', showfliers=False)
    plt.ylabel ("Concentração ($\mu g/m^3$)" if not ENGLISH else "Concentration ($\mu g/m^3$)")
    plt.xlabel ("Mês" if not ENGLISH else "Month")
    plt.xticks(rotation=45)
    if ENGLISH:
        plt.gca().legend().texts[0].set_text("MP10")
    # plt.legend()
    
    plt.tight_layout()
    plt.savefig(PASTA + "material_particulado"+EXT)

def vento_geracao():
    plt.figure(figsize=FIGSIZE)
    x = dados["Vel_Vento"]
    y = pard.E_ac_h.reset_index(drop=True)
    sns.scatterplot(x=x, y=y)
    sns.regplot(x=x, y=y, scatter=False, color="green")
    
    if SHOW_TITLE:
        plt.title ("Comparação entre velocidade do vento e geração")
    plt.xlabel ("$V_{vento}$ ($m/s$)")
    plt.ylabel ("$E_{AC}$ ($kWh$)")
    
    plt.tight_layout()
    plt.savefig(PASTA + "vento_geracao"+EXT)

def regressao_kopke():
    plt.figure(figsize=FIGSIZE)
    x = dados["Rad_Global"]
    y = dados["Radiacao_original (W/m2)"]
    sns.scatterplot(x=x, y=y)
    sns.regplot(x=x, y=y, scatter=False, color="green")
    
    if SHOW_TITLE:
        plt.title ("Comparação dos piranômetros")
    plt.xlabel ("$G_I$ - Machado e Barbosa ($W$)")
    plt.ylabel ("$G_I$ - CMP11 ($W$)")
    
    plt.tight_layout()
    plt.savefig(PASTA + "regressao_kopke"+EXT)
    
# TODO: sns.jointplot(x=rad_d/1000, y=E_ac_d, kind="hist", bins=50)

def regressao_luizinho():
    fig, ax = plt.subplots(figsize=FIGSIZE_HALF)
    
    x = dados.temp
    y = dados["Temperatura Original (C)"]
    
  
    sns.scatterplot(x=x, y=y)
    p = sns.regplot(x=x,  y=y, scatter = False, color='green')

    if SHOW_TITLE:
        plt.title("Distribuição da diferença entre as temperaturas do módulo e do ar" if not ENGLISH else "Distribution of the difference between module and air temperatures")
    else:
        _r2(x,y)
    
    plt.tight_layout()
    if ENGLISH:
        plt.xlabel("??")
        plt.ylabel("??")
    else:
        plt.xlabel("$T_\mathit{amb}$ Estação Parceira (°C)")
        plt.ylabel("$T_\mathit{amb}$ CETESB (°C)")
    _legenda_equacao_linear(p)
    plt.legend()
    plt.savefig(PASTA + 'regressao_luizinho'+EXT)

def histograma_falhas():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    df = pd.DataFrame({
        "hour": dados["Time"].dt.hour,
        "time": dados["Time"]
    })[~dados["Radiacao (W/m2)"].isna()]
    sns.histplot(data=df, y='hour', x='time', bins=(12,14), cbar=True, cmap="mako")
    ax.xaxis.set_major_formatter(myFmt)
    months = MonthLocator()  # every month
    ax.xaxis.set_major_locator(months)
    plt.yticks(0.5+np.arange(5,20), np.arange(5,20))
    plt.xticks(rotation=45)
    plt.xlabel("Tempo")
    plt.ylabel("Hora do dia")
    plt.tight_layout()
    plt.savefig(PASTA + 'histograma_falhas'+EXT)
    
def heatmap_rad():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    rad = dados["Radiacao (W/m2)"]
    rad.index = dados['Time']
    grouped = rad.groupby([rad.index.year, rad.index.month, rad.index.hour]).mean().rename_axis(index=["year","month","hour"]).reset_index()
    grouped['day'] = 1
    grouped['date'] = pd.to_datetime(grouped[['month', 'day', 'year']])
    matrix = grouped.pivot('hour','date', "Radiacao (W/m2)")
    sns.heatmap(matrix.iloc[::-1], cmap="coolwarm", cbar_kws={'label': '$G_I$ médio ($kW/m^2$)'})
    ax.set_xticklabels(matrix.columns.to_series().dt.strftime('%m/%y'))
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.xlabel("Tempo")
    plt.ylabel("Hora do dia")
    plt.tight_layout()
    plt.savefig(PASTA + 'heatmap_rad'+EXT)
    
def heatmap_temp():
    col = "Temperature(C)"
    fig, ax = plt.subplots(figsize=FIGSIZE)
    rad = dados[col]
    rad.index = dados['Time']
    grouped = rad.groupby([rad.index.year, rad.index.month, rad.index.hour]).mean().rename_axis(index=["year","month","hour"]).reset_index()
    grouped['day'] = 1
    grouped['date'] = pd.to_datetime(grouped[['month', 'day', 'year']])
    matrix = grouped.pivot('hour','date', col)
    sns.heatmap(matrix.iloc[::-1], cmap="coolwarm", cbar_kws={'label': '$T$ médio ($\textdegree C$)'})
    ax.set_xticklabels(matrix.columns.to_series().dt.strftime('%m/%y'))
    plt.xticks(rotation=45)
    plt.yticks(rotation=0)
    plt.xlabel("Tempo")
    plt.ylabel("Hora do dia")
    plt.tight_layout()
    plt.savefig(PASTA + 'heatmap_temp'+EXT)


def todos():
    temp_modfv_ar_tempo()
    temp_modfv_ar_prop()
    energiatotalprod_tempo()
    energia_tempo()
    potencia_umidade()
    vvento_temp_modfv()
    potencia_sombreamento()
    potencia_radiacao()
    radiacao_cetesb_vs_piranometro()
    energia_diaria_X_umidade_media_santos()
    energia_diaria_X_umidade_media_pp()
    proporcao_temperatura_X_vvento()
    radiacao_ao_longo_do_tempo()
    guilherme_alvaro_vs_pp()
    comparacao_solergo_radiacao()
    comparacao_solergo_energia()
    # influencias_temp_modfv_vs_ar()
    histograma_delta_temp()
    temp_ambiente_vs_delta_temp_dias_ensolarados()
    delta_temp_vs_radiacao()
    irradiancia_vs_potencia()
    razao_temp_vs_irradiancia()
    material_particulado()
    regressao_luizinho()
    heatmap_rad()
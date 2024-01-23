import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from datetime import datetime
import os

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])
hoje = datetime.today()
PASTA = "Gráficos/%s - Gráficos %s/" % (hoje.strftime('%Y%m%d'), hoje.strftime('%d.%m.%Y'))
EXT = ".png"
FIGSIZE = (8,5) # largura, altura

DIA_CEU_CLARO_MAXIMO =(2020,9,10)
DIA_CEU_CLARO_FRACO = (2020,9,16)
DIA_SOMBRA = (2020,9,28)
AREA_SISTEMA = 7.76

dias = [('Sombra', DIA_SOMBRA), ('Céu Claro', DIA_CEU_CLARO_MAXIMO), ('Céu Claro', DIA_CEU_CLARO_FRACO)]

if not os.path.isdir(PASTA):
    os.mkdir(PASTA)

sns.set()
plt.rcParams["font.family"] = "serif"
 
plt.figure(figsize=FIGSIZE)   
  
for (desc, (y,m,d)) in dias:
    fig, ax = plt.subplots(figsize=FIGSIZE)
    mask = (dados.Time.dt.day == d) & (dados.Time.dt.month == m) & (dados.Time.dt.year == y)
    dados_do_dia = dados[mask]

    sns.lineplot(y= dados_do_dia['Power(W)']/AREA_SISTEMA, x = dados_do_dia.Time, label="Sistema FV")
    sns.lineplot(y= dados_do_dia['Radiacao (W/m2)'], x = dados_do_dia.Time, label="Piranômetro")
     
    myFmt = DateFormatter("%H")
    ax.xaxis.set_major_formatter(myFmt)
    fig.autofmt_xdate()
     
    if SHOW_TITLE:
        plt.title ("Relação de potência ao longo de um dia (%02d/%02d/%04d) - %s" % (d,m,y, desc))
    plt.xlabel ("Tempo (h)")
    plt.ylabel ("Potência por área ($W/m^2$)")
    plt.legend ()
    
    plt.tight_layout()
        
    plt.savefig(PASTA + 'relacao_potencia_diaria_' + ("%04d-%02d-%02d" % (y,m,d)) + EXT)
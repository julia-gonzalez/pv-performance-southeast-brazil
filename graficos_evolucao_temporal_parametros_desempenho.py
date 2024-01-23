# -*- coding: utf-8 -*-
import seaborn as sns
import matplotlib.pyplot as plt
import parametros_desempenho as pard
import pandas as pd
from datetime import datetime
import os
import piranometro
import numpy as np

rad_cetesb_piranometro = piranometro.combinar_cetesb()

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])
dados = dados.resample('1D', on='Time').mean()

hoje = datetime.today()
PASTA = "Gráficos/%s - Gráficos %s/Parâmetros de desempenho - Evolução/" % (hoje.strftime('%Y%m%d'), hoje.strftime('%d.%m.%Y'))

# if not os.path.isdir(PASTA):
#     os.mkdir(PASTA)


from config_graficos import EXT, FIGSIZE, FIGSIZE_SM, ENGLISH, SHOW_TITLE, SHOW_LEGEND

rad = dados['Radiacao (W/m2)']
def make(p, lbl):
    p_ms = [p.min(), p.max()]
    rad_ms = [rad.min(), rad.max()]
    
    def inverse(x_rad): # rad to p
        return np.interp(x_rad, rad_ms, p_ms)
    
    def forward(x_p): # p to rad
        return np.interp(x_p, p_ms, rad_ms)
    plt.figure(figsize=FIGSIZE)
    rad.apply(inverse).plot.area(color="C1")
    p.plot()
    plt.xlabel('Tempo')
    plt.ylabel(lbl)
    ax = plt.gca()
    ax.secondary_yaxis('right', functions=(forward, inverse))
    plt.title(lbl)
    plt.savefig(PASTA + "evolucao_"+lbl+EXT)
    plt.tight_layout()
    plt.show()


remove_outlier = pard.P_R_d < 200
# make(pard.P_R_d[remove_outlier], '$PR$ (%)')
# make(pard.Y_f_d[remove_outlier], '$Y_f$')
# make(pard.Y_r_d[remove_outlier], '$Y_r$')
# make(100*pard.N_PV_d, '$\eta_{PV}$')

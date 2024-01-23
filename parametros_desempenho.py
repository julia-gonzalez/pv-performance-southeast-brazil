# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 18:12:44 2020

@author: User
"""

import pandas as pd
import piranometro
import numpy as np

#Potência instalada (kWp) = P0
P0 = (330*4)/1000

#Condição STC - Irradiância de referência de 1000W/m²
G_STC = 1000

#Condição NOCT - Irradiância de referência de 800W/m²
#G_NOCT = 800

#Área ocupada pelos módulos FVs (Am):
Am = 7.76

dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"], index_col="Time")
def subtracao(dias):
    diff = dias.iloc[1] - dias.iloc[0]
    if(diff < -0.001): # Provavelmente inicio de proximo dia
        if dias.iloc[1] > 0.5: # remove flutuacoes estranhas
            return np.nan
        return dias.iloc[1]
    return diff


#Irradiação solar no plano é HI, aqui chamado de "rad_h", durante uma hora
rad_h = dados['Radiacao (W/m2)'].copy()
dias_inicio_ou_fim_falha = ["2020-10-23", "2021-07-18", "2021-08-06"]
for d in dias_inicio_ou_fim_falha:
    rad_h[d] = np.nan
# rad_h[rad_h < 50] = np.nan


#Energia Produzida horária (Eac,h):
E_ac_h =  dados["Generation Today(kWh)"].rolling(window=2).apply(subtracao)
E_ac_h[rad_h.isna()] = np.nan
rad_h[E_ac_h.isna()] = np.nan


#Daqui pra frente divide-se pela condição STC (G_STC), de 1000 W/m²

#Produtividade de Referência (Y_r):
#Produtividade de Referência (Y_r) por hora:
#Produtividade de Referência (Y_r) por dia:
rad_d = rad_h.resample("1D").sum()

#Produtividade de Referência (Y_r) por mês:
rad_m = rad_h.resample("1M").sum()

#Energia Produzida diária (Eac,d):
E_ac_d = E_ac_h.resample('1d').sum()

#Energia Produzida mensal (Eac,m):
E_ac_m =  E_ac_d.resample('1M').sum()



Y_r_d = rad_d/G_STC
Y_r_m = rad_m/G_STC
Y_r_h = rad_h/G_STC


#Produtividade Final (Y_f):
#Produtividade Final (Y_f) por hora:
Y_f_h = (E_ac_h / P0)

#Produtividade Final (Y_f) por dia:
Y_f_d = (E_ac_d / P0)

#Produtividade Final (Y_f) por mês:
Y_f_m = (E_ac_m / P0)


#ENERGIA PRODUZIDA (Eac)



#ENERGIA RECEBIDA (Edc): P = I * U
#Energia Recebida horária (Edc,h):     
E_dc_h = (dados["V MPPT 1(V)"] * dados["I MPPT 1(A)"]/1000).rolling(window=2).mean()
E_dc_h[E_ac_h.isna()] = np.nan

#Energia Recebida diária (Edc,d):
E_dc_d =  E_dc_h.resample("1D").sum()

#Energia Recebida mensal (Edc,m):
E_dc_m =  E_dc_d.resample('1M').sum()

#PRODUTIVIDADE(Y)

#Produtividade do Arranjo Fotovoltaico (Y_A): 
#Produtividade do Arranjo Fotovoltaico (Y_A) por hora:
Y_A_h = E_dc_h/P0

#Produtividade do Arranjo Fotovoltaico (Y_A) por dia:
Y_A_d = E_dc_d/P0

#Produtividade do Arranjo Fotovoltaico (Y_A) por mês:
Y_A_m = E_dc_m/P0


#PERDAS
#Perda de Captura de Arranjo (L_c):
#Perda de Captura de Arranjo (L_c) por hora:
L_c_h = Y_r_h - Y_A_h

#Perda de Captura de Arranjo (L_c) por dia:
L_c_d = Y_r_d - Y_A_d

#Perda de Captura de Arranjo (L_c) por mês:
L_c_m = Y_r_m - Y_A_m

#Perda de Sistema (L_S): 
#Perda de Sistema (L_S) por hora:
L_S_h = Y_A_h - Y_f_h

#Perda de Sistema (L_S) por dia:
L_S_d = Y_A_d - Y_f_d

#Perda de Sistema (L_S) por mês:
L_S_m = Y_A_m - Y_f_m


#Perdas totais (L_T): 
#Perdas totais (L_T) por hora:
L_T_h = Y_r_h - Y_f_h

#Perdas totais (L_T) por dia:
L_T_d = Y_r_d - Y_f_d

#Perdas totais (L_T) por mês:
#L_T_m = L_c_m + L_S_m
L_T_m = Y_r_m - Y_f_m

#EFICIÊNCIA (N):
#EFICIÊNCIA DO MÓDULO FV (N_PV):
#Eficiência do módulo FV (N_PV) por hora:
N_PV_h = (100*E_dc_h)/(rad_h*Am)

#Eficiência do módulo FV (N_PV) por dia:
N_PV_d = (100*E_dc_d)/(rad_d*Am)

#Eficiência do módulo FV (N_PV) por mês:
N_PV_m = (100*E_dc_m)/(rad_m*Am)

#EFICIÊNCIA DO SISTEMA FV (N_SYS):
#Eficiência do sistema FV (N_PV) por hora:
N_SYS_h = (100*E_ac_h)/(rad_h*Am/1000)

#Eficiência do sistema FV (N_PV) por dia:
N_SYS_d = (100*E_ac_d)/(rad_d*Am/1000)

#Eficiência do sistema FV (N_PV) por mês:
N_SYS_m = (100*E_ac_m)/(rad_m*Am/1000)

#EFICIÊNCIA DO INVERSOR (N_INV):
#Eficiência do inversor (N_INV) por hora:
N_INV_h = (100*E_ac_h)/E_dc_h

#Eficiência do inversor (N_INV) por dia:
N_INV_d = (100*E_ac_d)/E_dc_d

#Eficiência do inversor (N_INV) por mês:
N_INV_m = (100*E_ac_m)/E_dc_m

#PR (P_R):
#PR por hora:
P_R_h = (100*Y_f_h)/Y_r_h

#PR por dia:
P_R_d = (100*Y_f_d)/Y_r_d

#PR por mês:
P_R_m = (100*Y_f_m)/Y_r_m

#PR_A
PR_A_h = (100*Y_A_h)/Y_r_h
PR_A_d = (100*Y_A_d)/Y_r_d
PR_A_m = (100*Y_A_m)/Y_r_m

#FATOR DE CAPACIDADE(CF): na verdade, ele é ideal para a produção de CA durante um ano, mas fiz o somatório até hoje
#CF por dia:
CF_d = ((100*E_ac_d)/(P0*24)).rename("CF")
CF_d[CF_d == 0] = np.nan

#CF por mês:
CF_m = CF_d.resample('1M').mean()
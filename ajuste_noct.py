import pandas as pd
dados = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])

########################
# Ajuste da Tensão Voc #
########################
# temp_maxima_por_mes = dados.resample('1M', on='Time')['Temperature(C)'].max()

# temp_exp = temp_maxima_por_mes['2020-10-31'] # outubro

# beta = -0.31/100

# temp_noct = 45
# voc_noct = 42.3
# voc_exp = 42.8 # foi a referencia do artigo "Ajuste das variaveis de saida do modulo"

# delta_t = temp_exp - temp_noct
# fc = beta * delta_t

# voc_ajustada = voc_exp - fc * voc_noct


##########################
# Ajuste da Corrente ISC #
##########################

alfa = 0.05/100
t_stc = 25
g_stc = 1000
i_maxima_por_mes = dados.resample('1M', on='Time')['I MPPT 1(A)'].max()
isc_catalogo = 7.5

isc_exp = i_maxima_por_mes['2020-10-31']
argexp = dados[dados['I MPPT 1(A)'] == isc_exp].iloc[0]
t_exp = argexp['Temperature(C)']
g_exp = argexp['Radiacao (W/m2)']
isc_ajustada = isc_exp * (1 - alfa * (t_stc - t_exp)) * g_stc/g_exp
print("O ISC ajustado foi %.2fA" % isc_ajustada)
print("Comparado com o orignal de %.2fA, temos uma diferença de %.2fA" % (isc_catalogo, (isc_ajustada- isc_catalogo)))
print("Portanto, o erro foi de %.2f%%" % (100 * (isc_ajustada- isc_catalogo)/isc_catalogo))
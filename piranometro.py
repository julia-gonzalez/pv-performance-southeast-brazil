import pandas as pd
import os


CONSIDERAR_RADIACAO_CETESB = False

def pegar_data(df):
    hora_min = df[3].astype(str).str.zfill(4)
    ano = df[1].astype(str)
    dia = df[2].astype(str)
    hora = hora_min.str.slice(0,2).astype(int)
    minuto = hora_min.str.slice(2,4).astype(int)
    
    data = pd.to_datetime(ano + " " + dia, format="%Y %j")
    deltas = pd.to_timedelta(hora-3, 'hours') + pd.to_timedelta(minuto, 'minutes')
    return data + deltas

def carregar_todos():
    return pd.concat([
        pd.read_csv('dados-piranometro/%s' % f, header=None)
        for f in os.listdir('dados-piranometro/')
        ])
        

def radiacao():
    dados = carregar_todos()
    tratados = pd.DataFrame()
    # Parece que as variaveis 7 e 5 medem a radiação em kW/m².
    
    tratados['Radiacao (W/m2)'] = dados[5] * 1000
    tratados.index = pegar_data(dados)
    tratados = tratados[tratados.index > '2020-09-08'] # antes do dia 09 de setembro, há algumas falhas
    return tratados
def radiacao_hora():
    return radiacao().resample('1h').mean()
def radiacao_dia():
    return radiacao().resample('1d').sum()

def combinar_cetesb():
    rad = pd.DataFrame()
    if CONSIDERAR_RADIACAO_CETESB:
        cetesb = pd.read_csv("dados-totais.csv", parse_dates = ["Time"])
        rad['Radiacao (W/m2)'] = cetesb['RADG(Radiação Solar Global) - W/m2 - Guilherme Alvaro']
        rad.index = cetesb.Time
        rad['Fonte'] = 'CETESB'
    pir = radiacao_hora()
    pir['Fonte'] = "Piranômetro"
    return pir.combine_first(rad)
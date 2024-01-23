import pandas as pd
import os
import piranometro
from sklearn.linear_model import LinearRegression

def ler_kopke():
    return pd.concat([
    pd.read_csv(f'Dados Henrique Kopke/{d}', 
                encoding='latin-1', sep=';', 
                decimal=',', parse_dates=[['DATE', 'TIME']], 
                infer_datetime_format=True, dayfirst=True) 
        for d in os.listdir('Dados Henrique Kopke')]).resample('60min', on="DATE_TIME").mean().loc['2021-01-27':]

def ler_luizinho():
    return pd.read_csv('temperatura_luizinho.csv', index_col=0, parse_dates=[0]).resample('1h').mean()

# def preenche_radiacao_faltantes(kopke, rad):
#     rad['Radiacao_original (W/m2)'] = rad['Radiacao (W/m2)']
#     rads = pd.DataFrame({'kopke': kopke.Rad_Global, 'piranometro': rad['Radiacao (W/m2)']}).dropna()
#     linha = LinearRegression().fit(rads[['kopke']], rads['piranometro'])
#     X = kopke[rad['Radiacao (W/m2)'].isna()].Rad_Global.dropna()
#     y = linha.predict(X.values.reshape(-1,1))
#     rad.loc[X.index, 'Radiacao (W/m2)'] = y
#     rad.loc[X.index, 'Fonte'] = 'RegressaoKopke'
#     return rad

def preenche_temp_faltantes(luizinho, t):
    t['Temperatura Original (C)'] = t['TEMP(Temperatura do Ar) - °C']
    temps = pd.DataFrame({'luizinho': luizinho.temp, 'cetesb': t['TEMP(Temperatura do Ar) - °C']}).dropna()
    linha = LinearRegression().fit(temps[['luizinho']], temps['cetesb'])
    X = luizinho[t['TEMP(Temperatura do Ar) - °C'].isna()].temp.dropna()
    y = linha.predict(X.values.reshape(-1,1))
    t.loc[X.index, 'TEMP(Temperatura do Ar) - °C'] = y
    t["FonteTemp"] = "CETESB"
    t.loc[X.index, 'FonteTemp'] = 'RegressaoLuizinho'
    return t

def preenche_radiacao_faltantes_media_mes(df):
    df['Radiacao_original (W/m2)'] = df['Radiacao (W/m2)']
    for month in [7,8,10]:
        m = df[df.index.month == month]
        media_rad = m.groupby(m.index.hour)['Radiacao (W/m2)'].mean().to_dict()
        idx = m.index[m['Radiacao (W/m2)'].isna()]
        mask = idx.hour.map(lambda h: media_rad[h])
        df.loc[idx,'Radiacao (W/m2)'] = mask.values
        df.loc[idx, 'Fonte'] = 'MediaMes'
    return df

def tratar_dados():
    phb = pd.concat([pd.read_csv("dados-phb/"+arquivo, parse_dates = ["Time"]) for arquivo in os.listdir('dados-phb')])
    cetesb = pd.read_csv('cetesb.csv', parse_dates = ["Data"], dayfirst=True, decimal=",")
    cetesb['DataHora'] = cetesb.Data + pd.to_timedelta(cetesb.Hora.str[:2].astype(int), 'hours')
    
    phb.set_index('Time', inplace=True)
    
    #Removemos dados da bateria (já que não tem bateria)
    phb.drop(inplace=True, columns=['Unnamed: 0'])
    
    cetesb.set_index('DataHora', inplace=True)
    
    media_horaria_phb = phb.resample("1h").mean().dropna()
    media_horaria_phb['Generation Today(kWh)'] = phb['Generation Today(kWh)'].resample('1h').last().dropna()
    cetesb_correspondente = cetesb.reindex(media_horaria_phb.index)
    
    dados_totais = pd.concat([media_horaria_phb, cetesb_correspondente], axis=1).drop(['RADUV(Radiação Ultra-violeta) - W/m2', 'Data', 'Hora'], axis=1).astype(float)
    #Removemos a coluna 'RADUV(Radiação Ultra-violeta, pois estava sem valor algum da CETESB
    
    dados_totais = dados_totais[dados_totais.index >= "2020-10-01"] # remove dados anteriores a outubro/2020 (defesa)
    dados_totais = dados_totais[dados_totais.index < "2021-10-01"] # remove dados posteriores a outubro/2021 (defesa)
    
    # Atualizacao da PHB :(
    dados_totais.rename(inplace=True, columns={
        "Temperature(℃)": "Temperature(C)",
        "Total Generation(kWh)": "ETotal(kWh)",
        "Today Generation(kWh)": "Generation Today(kWh)",
        })
    
    
    rad = piranometro.combinar_cetesb().reindex(dados_totais.index)
    kopke = ler_kopke().reindex(dados_totais.index)
    luizinho = ler_luizinho().reindex(dados_totais.index)
    # rad = preenche_radiacao_faltantes(kopke, rad)
    d = pd.concat([dados_totais, kopke, luizinho, rad], axis=1)
    d = preenche_temp_faltantes(luizinho, d)
    # d = d[(d.index.hour >= 8) & (d.index.hour <= 16)]
    
    
    # d = preenche_radiacao_faltantes_media_mes(d)
    d.to_csv("dados-totais.csv")
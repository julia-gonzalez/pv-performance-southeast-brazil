import pandas as pd
import piranometro
import matplotlib.pyplot as plt
import datetime as d
import numpy as np

MES = 10
DIA = 28

def entre(df, inicio, fim):
    return df[(df.index > inicio) & (df.index < fim)]

hora = piranometro.radiacao_hora()
minuto = piranometro.radiacao()

inicio = f"2020-{MES}-{DIA} 00:00"
fim = f"2020-{MES}-{DIA+1} 00:00"

hora = entre(hora, inicio, fim)
hora_defasada = hora.copy()
hora_defasada.index = hora.index + d.timedelta(minutes=59)
hora_final = pd.concat([hora, hora_defasada]).sort_index()
minuto = entre(minuto, inicio, fim)


plt.figure(figsize=(8,5))
plt.plot(minuto, label="Dados brutos (minuto)")
plt.plot(hora_final, label="Média horária")
plt.gcf().autofmt_xdate()
plt.ylabel("$W/m^2$")
plt.title("Radiacao no dia %02d/%02d/2020" % (DIA, MES))
plt.legend()
plt.tight_layout()
plt.show()

print("Soma das alturas dos segmentos laranjas: %.5f" % hora.sum()[0])

auc = np.trapz(minuto['Radiacao (W/m2)']) / 60

print("Área sob a curva: %.5f" % auc)
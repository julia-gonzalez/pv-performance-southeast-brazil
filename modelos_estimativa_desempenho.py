import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

dados = pd.read_csv("./dados-totais.csv", parse_dates = ["Time"])
y_hat = dados['Power(W)']

# PVUSA
dados_pvusa = pd.DataFrame({
        'G_I': dados['Radiacao (W/m2)'],
        'G_I^2': dados['Radiacao (W/m2)']**2,
        'G_I*S_W': dados['Radiacao (W/m2)']*dados['VV(Velocidade do Vento) - m/s'],
        'G_I*T_Amb': dados['Radiacao (W/m2)']*dados['TEMP(Temperatura do Ar) - °C'],
    })
X_pvusa = dados_pvusa[dados_pvusa.G_I >= 500].dropna()
y_hat_pvusa = y_hat.reindex(X_pvusa.index)
pvusa = LinearRegression(fit_intercept=False)
pvusa.fit(X_pvusa, y_hat_pvusa)

dados_dias = pd.DataFrame({
        'G_I': dados['Radiacao (W/m2)'],
        '(G_I/T_Amb)^2': (dados['Radiacao (W/m2)']/dados['TEMP(Temperatura do Ar) - °C'])**2,
        'G_I*T_Amb': dados['Radiacao (W/m2)']*dados['TEMP(Temperatura do Ar) - °C'],
    })

X_dias = dados_dias[dados_dias.G_I >= 500].dropna()
y_hat_dias = y_hat.reindex(X_dias.index)

dias = LinearRegression(fit_intercept=False)
dias.fit(X_dias, y_hat_dias)

table = pd.DataFrame([
    [pvusa.score(X_pvusa, y_hat_pvusa)] + list(pvusa.coef_),
    [dias.score(X_dias, y_hat_dias)] + list(dias.coef_) + [np.nan],
    ], index=["PVUSA", "Modelo II"], columns=["$R^2$", "$a$", "$b$", "$c$", "$d$"])

print(table.to_latex(escape=False, na_rep="---", float_format="%.5f"))
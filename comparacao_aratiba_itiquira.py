import pandas as pd
import parametros_desempenho as pard

tabela = pd.DataFrame([{
        "Localização": "Aratiba",
        "Energia (kWh/ano)": 10839,
        "$P_0$ (kWp)": 9,
        "PR (\%)": 78.7,
        "$Y_r$ (kWh/kWp)": 1214
    },{
        "Localização": "Itiquira",
        "Energia (kWh/ano)": 13523,
        "$P_0$ (kWp)": 9,
        "PR (\%)": 74.9,
        "$Y_r$ (kWh/kWp)": 1514
    },{
       "Localização" : "UNIFESP",
       "Energia (kWh/ano)": pard.E_ac_m.sum(),
       "$P_0$ (kWp)": 1.3,
       "PR (\%)": pard.P_R_m.mean(),
       "$Y_r$ (kWh/kWp)": pard.Y_f_m.sum(),
    }])

tabela.insert(3, "Energia/P0 (kWh/ano$\cdot$kWp)", tabela["Energia (kWh/ano)"] / tabela["$P_0$ (kWp)"])
tabela = tabela.set_index("Localização")
print(tabela.transpose().to_latex(escape=False, float_format="%.1f"))
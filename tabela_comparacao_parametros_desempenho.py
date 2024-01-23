import parametros_desempenho as pard
import pandas as pd

def make_row(name, p):
    return [name, p.mean(), p.max(), p.index[p.argmax()].strftime("%m"), p.min(), p.index[p.argmin()].strftime("%m")]

params = [
        ("$Y_r$", pard.Y_r_m),
        ("$Y_f$", pard.Y_f_m),
        ("$L_S$", -pard.L_S_m),
        ("$PR$", pard.P_R_m),
        ("$CF$", pard.CF_m),
        ("$\eta_{SYS}$", pard.N_SYS_m),
    ]
table = [make_row(*p) for p in params]
table = pd.DataFrame(table, columns=["Parameters", "Mean", "Maximum", "Max Month", "Minimum", "Min Month"])
print(table)
print(table.to_latex(float_format="%.1f", escape=False, index=False))
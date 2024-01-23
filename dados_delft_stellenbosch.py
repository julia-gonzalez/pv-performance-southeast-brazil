import numpy as np
import parametros_desempenho as pard

import pandas as pd

ID_ARATIBA = 3047
ID_ITIQUIRA = 16345
ID_NATAL = 50307 

AREA_ARATIBA_ITIQUIRA = 38*1.63

dni = pd.read_csv('./dados-aratiba-itiquira/direct_normal_means_sedes-munic.csv', sep=';', index_col=0)
hi = pd.read_csv('./dados-aratiba-itiquira/tilted_latitude_means_sedes-munic.csv', sep=';', index_col=0)

def get_dni(city_id):
    return dni.loc[city_id].values[-12:]

def get_hi(city_id):
    return hi.loc[city_id].values[-12:]

days_in_each_month = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
month_abbr = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

delft_yr = np.array([39.3, 52, 113.7, 146.5, 166.7, 160.6, 162.3, 146.2, 110.3, 73.9, 41.4, 29.4])/days_in_each_month
delft_yf = np.array([33, 43.9, 94.5, 119.4, 133.5, 127.2, 126.9, 114.9, 88.5, 60.4, 33.9, 23.9])/days_in_each_month
delft_ls = np.array([6.3, 8.1, 19.1, 27.1, 33.2, 33.4, 35.3, 31.3, 21.9, 13.5, 7.6, 5.5])/days_in_each_month
delft_pr = np.array([0.84, 0.84, 0.83, 0.82, 0.80, 0.79, 0.78, 0.79, 0.80, 0.82, 0.82, 0.81])
delft_cf = np.array([4.4, 6.4, 12.7, 12.9, 17.9, 17.7, 17.1, 15.4, 12.3, 8.1, 4.7, 3.2])
delft_nsys = np.array([13, 13.1, 12.9, 12.7, 12.5, 12.3, 12.2, 12.2, 12.5, 12.7, 12.7 ,12.6])
delft_temp = np.array([4, 4, 7, 9, 13, 15, 18, 18, 15, 11, 7, 5])
delft_dni = np.array([35.8,51.4,81.4,111.1,133.3,127.8,125.9,106.8,79.6,58,34.1,27.8,])/days_in_each_month

stellenbosch_yr = np.array([248.2, 227.3, 205.1, 162.9, 120.5, 100.1, 117.2, 130.4, 159.7, 208.5, 225.2, 248.6])/days_in_each_month
stellenbosch_yf = np.array([178.9, 164.1, 150.8, 123.8, 94.5, 80.2, 94, 103.1, 123.7, 156.6, 166.2, 180.1])/days_in_each_month
stellenbosch_ls = np.array([69.3, 63.2, 54.3, 39.1, 25.9, 19.9, 23.2, 27.3, 36, 52, 59, 68.5])/days_in_each_month
stellenbosch_pr = np.array([0.72, 0.72, 0.74, 0.76, 0.78, 0.80, 0.80, 0.79, 0.77, 0.75, 0.74, 0.72])
stellenbosch_cf = np.array([24, 23.7, 20.3, 17.2, 12.7, 11.1, 12.6, 13.9, 17.2, 21, 23.1, 24.2])
stellenbosch_nsys = np.array([11.1, 11.1, 11.3, 11.7, 12.1, 12.3, 12.3, 12.2, 11.9, 11.6, 11.4, 11.1])
stellenbosch_temp = np.array([22, 22, 21, 18, 16, 13, 13, 13, 15, 17, 19, 21])
stellenbosch_dni = np.array([281.8,239.5,219.5,171.3,126.4,109,124.7,128.3,150.9,204.4,233.3,267.3,])/days_in_each_month

P0_ARATIBA_ITIQUIRA = 8.93
G_STC = 1000
KILO = 1000

aratiba_dni = get_dni(ID_ARATIBA)/KILO
aratiba_hi = np.array([175.8, 144.6, 154.0, 127.2, 94.6, 92.8, 86.0, 142.9, 136.4, 131.2, 128.8, 141.3])
aratiba_yr = days_in_each_month*aratiba_hi/G_STC
aratiba_temp = np.array([25.3, 24.9, 21.7, 21.9, 15.5, 14.5, 15.2, 19.0, 18.5, 20.9, 21.9, 23.7])
aratiba_yf = np.array([127.8, 109.7, 119.3, 96.2, 81.3, 79.2, 73.2, 116.9, 109.0, 102.0, 94.3, 104.9])/days_in_each_month
aratiba_pr =100*aratiba_yf/aratiba_yr
aratiba_cf = 100/24 * aratiba_yf
aratiba_nsys = days_in_each_month*100*aratiba_yf*P0_ARATIBA_ITIQUIRA/(aratiba_hi*AREA_ARATIBA_ITIQUIRA)


itiquira_dni = get_dni(ID_ITIQUIRA)/KILO
itiquira_hi = np.array([157.3, 162.8, 170.3, 177.4, 164.6, 153.3, 162.2, 204.4, 169.6, 174.6, 165.1, 161.2])
itiquira_yr = days_in_each_month*itiquira_hi/G_STC
itiquira_temp = np.array([26.1, 26.8, 26.3, 26.5, 24.1, 24.3, 24.2, 27.9, 28.4, 28.3 ,27.4, 26.7])
itiquira_yf = np.array([118.7, 119.3, 123.4, 125.8, 119.9, 125.2, 126.2, 153.0, 127.9, 130.1, 123.7, 121.2])/days_in_each_month
# itiquira_dni = np.array([5.4, 5.8, 5.3, 5.3, 4.5, 4.9, 4.3, 5.7, 5.3, 5.6, 5.8, 5.6])
# itiquira_yr = itiquira_dni/1000
itiquira_pr =100*itiquira_yf/itiquira_yr
itiquira_cf = 100/24 * itiquira_yf
itiquira_nsys = days_in_each_month*100*itiquira_yf*P0_ARATIBA_ITIQUIRA/(itiquira_hi*AREA_ARATIBA_ITIQUIRA)

P0_NATAL = 56.4
AREA_NATAL = 240 * 1.642*0.992
natal_eac = np.array([8141,7598,8521,7635,6921,6070,6768,7932,7995,8727,8337,8319])
natal_yf = natal_eac/(P0_NATAL*days_in_each_month)
natal_dni = get_dni(ID_NATAL)/KILO
natal_hi = get_hi(ID_NATAL)/days_in_each_month
natal_yr = days_in_each_month*natal_hi/G_STC
natal_pr =100*natal_yf/natal_yr
natal_cf = 100/24 * natal_yf
natal_temp = np.array([27.8, 27.7, 27.5, 27.4, 26.5, 26.0, 25.5, 25.7, 26, 26.5, 26.7, 27.5, 27.7])
natal_nsys = days_in_each_month*100*natal_yf*P0_NATAL/(natal_hi*AREA_NATAL)




santos_temp = np.array([24, 24, 23, 22, 19, 18, 18, 19, 19, 21, 22, 23])
santos_dni = np.array([89.9,95.1,100.6,100.9,99.6,92.1,101.5,99.4,66,68.6,72.9,85.7])/days_in_each_month

calculate = lambda x: ["%.1f" %x.mean(), "%.1f" %x.max(), x.index[x.argmax()], "%.1f" %x.min(), x.index[x.argmin()]]

calc_np = lambda x: " & ".join(["%.1f" % x.mean(),"%.1f" % x.max(), month_abbr[x.argmax()], "%.1f" %x.min(), month_abbr[x.argmin()]])

print("Santos")
print("Yr", calculate(pard.Y_r_d.resample("1M").mean()))
print("Yf", calculate(pard.Y_f_d.resample("1M").mean()))
print("Ls", calculate(-pard.L_S_d.resample("1M").mean()))
print("DNI", calc_np(santos_dni))

print()
print("Delft")
print("Yr", calc_np(delft_yr))
print("Yf", calc_np(delft_yf))
print("Ls", calc_np(delft_ls))
print("DNI", calc_np(delft_dni))

print()
print("Stellenbosch")
print("Yr", calc_np(stellenbosch_yr))
print("Yf", calc_np(stellenbosch_yf))
print("Ls", calc_np(stellenbosch_ls))
print("DNI", calc_np(stellenbosch_dni))

print()
print("Aratiba")
print("Yr", calc_np(aratiba_yr))
print("Yf", calc_np(aratiba_yf))
print("PR", calc_np(aratiba_pr))
print("CF", calc_np(aratiba_cf))
print("Temp", calc_np(aratiba_temp))
print("DNI", calc_np(aratiba_dni))
print("n_sys", calc_np(aratiba_nsys))

print()
print("Itiquira")
print("Yr", calc_np(itiquira_yr))
print("Yf", calc_np(itiquira_yf))
print("PR", calc_np(itiquira_pr))
print("CF", calc_np(itiquira_cf))
print("Temp", calc_np(itiquira_temp))
print("DNI", calc_np(itiquira_dni))
print("n_sys", calc_np(itiquira_nsys))

print()
print("Natal")
print("Yr", calc_np(natal_yr))
print("Yf", calc_np(natal_yf))
print("PR", calc_np(natal_pr))
print("CF", calc_np(natal_cf))
print("Temp", calc_np(natal_temp))
print("DNI", calc_np(natal_dni))
print("n_sys", calc_np(natal_nsys))
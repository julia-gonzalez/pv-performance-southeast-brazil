import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import config_graficos as cg


if cg.ENGLISH:
   meses = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct","Nov", "Dec"]
else:
   meses = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out","Nov", "Dez"]
   
meses_estudados = ["Jan/21", "Fev/21", "Mar/21", "Abr/21", "Mai/21", "Jun/21", "Jul/21", "Ago/21", "Set/21", "Out/20", "Nov/20", "Dez/20"]


# MOVIMENTO PORTO
totais_movimentados = pd.DataFrame([
    #15       #16       17       18       19       20       21
    [7507230, 7834883, 7364575, 8996324, 9053996, 8313047, 9192069], #1
    [8541527, 9018599, 9676623, 9676243, 10031300, 10655788, 10926934], #2
    [10312506, 10905367, 10862308, 12243080, 11363045, 12796138, 15165555], #3 
    [9461437, 9754582, 10700406, 11746598, 10565304, 13486383, 13759247], #4
    [10083859, 10399451, 11397641, 10951693, 10993710, 13059420, 14082551], #5
    [9293424, 9865200, 11042382, 10851746, 11576036, 12364397, 13251003], #6
    [11080400, 10182378, 12053697, 11872362, 12744535, 13562345, 12555330], #7
    [11365789, 10661252, 12342511, 12482543, 12087569, 13732925, 12065663], #8
    [11000769, 9906676, 12243774, 11579406, 11569319, 12171362, 11851299], #9
    [11313396, 9146027, 11368212, 10253845, 12788883, 12479095],
    [9855418, 7754698, 10903041, 11662742, 11024909, 12120684],
    [10116125, 8386639, 9909852, 10843180, 10211886, 11863219]
    ], columns=[2015,2016,2017,2018,2019,2020,2021], index=meses).melt(ignore_index=False,var_name="ano",value_name="valor").reset_index()

totais_movimentados["mil_ton"] = totais_movimentados.valor/1_000_000

plt.subplots(figsize=cg.FIGSIZE)
sns.set_context(rc = {'patch.linewidth': 0.0})
sns.barplot(data=totais_movimentados, x="index", y="mil_ton", hue="ano")


plt.xlabel ("Mês")
plt.ylabel ("Total Movimentado ($10^6$ ton)")
plt.legend ()
plt.ylim(0,18)

plt.tight_layout()
plt.savefig('porto_movimento' + cg.EXT)


# GERAL - GRANEL
cols = ["%s_%s" % (conteudo, tipo) for conteudo in ["geral", "solidos_granel", "liquidos_granel", "total"] for tipo in ["longo_curso", "cabotagem", "soma"]]
importacao_2021 = pd.DataFrame([
    [1452885, 469256, 1922141, 1032148, 36007, 1068155, 430617, 55639, 486256, 2915650, 560902, 3476552],
    [1539078, 368089, 1907167, 998601, 37723, 1036324, 376727, 79383, 456110, 2914406, 485195, 3399601],
    [1830650, 362276, 2192926, 775989, 68935, 844924, 397484, 90701, 488185, 3004123, 521912, 3526035],
    [1581344, 369954, 1951298, 889336, 12240, 901576, 452649, 135132, 587781, 2923329, 517326, 3440655],
    [1721551, 423250, 2144801, 864248, 36004, 900252, 395701, 137356, 533057, 2981500, 596610, 3578110],
    [1603538, 354560, 1958098, 1048594, 44227, 1092821, 422495, 83148, 505643, 3074627, 481935, 3556562],
    [1749903, 322677, 2072580, 1044340, 35562, 1079902, 540054, 124108, 664162, 3334297, 482347, 3816644],
    [1836285, 308628, 2144913, 1199010, 50948, 1249958, 416540, 132261, 548801, 3451835, 491837, 3943672],
    [1678626, 308271, 1986897, 1266078, 74163, 1340241, 597999, 74561, 672560, 3542703, 456995, 3999698]],
    columns=cols, index=meses_estudados[:9]
    )
exportacao_2021 = pd.DataFrame([
    [2036080, 435817, 2471897, 2248854, 1453, 2250307, 384770, 608543, 993313, 4669704, 1045813, 5715517],
    [2365060, 333487, 2698547, 4007962, 3944, 4011906, 404000, 412880, 816880, 6777022, 750311, 7527333],
    [2639385, 405708, 3045093, 7489565, 8731, 7498296, 443342, 652789, 1096131, 10572292, 1067228, 11639520],
    [2396702, 370233, 2766935, 6637036, 2051, 6639087, 396288, 516282, 912570, 9430026, 888566, 10318592],
    [2383166, 384581, 2767747, 6855449, 10036, 6865485, 410282, 460927, 871209, 9648897, 855544, 10504441],
    [2497244, 407597, 2904841, 5691451, 3154, 5694605, 520163, 574832, 1094995, 8708858, 985583, 9694441],
    [2294974, 366965, 2661939, 4999238, 7584, 5006822, 512351, 557574, 1069925, 7806563, 932123, 8738686],
    [2473554, 385713, 2859267, 4252247, 6111, 4258358, 395420, 608946, 1004366, 7121221, 1000770, 8121991],
    [2464918, 378636, 2843554, 4000359, 7321, 4007680, 489795, 510572, 1000367, 6955072, 896529, 7851601
    ]],
    columns=cols, index=meses_estudados[:9]
    )
importacao_2020 = pd.DataFrame([
    [1418092, 445194, 1863286, 1150435, 32065, 1182500, 525202, 104832, 630034, 3093729, 582091, 3675820],
    [1471375, 385929, 1857304, 984353, 39655, 1024008, 717066, 108252, 825318, 3172794, 533836, 3706630],
    [1633723, 348620, 1982343, 1096471, 67056, 1163527, 614641, 82653, 697294, 3344835, 498329, 3843164]],
    columns=cols, index=meses_estudados[9:]
    )
exportacao_2020 = pd.DataFrame([
    [2560791, 382487, 2943278, 4801348, 2879, 4804227, 560116, 495654, 1055770, 7922255, 881020, 8803275],
    [2554225, 392310, 2946535, 4496244, 2171, 4498415, 475893, 493211, 969104, 7526362, 887692, 8414054],
    [2780073, 332875, 3112948, 3964217, 20014, 3984231, 437123, 485753, 922876, 7181413, 838642, 8020055]
    ],
    columns=cols, index=meses_estudados[9:]
    )

data = pd.DataFrame()
data["Geral - Importação"] = pd.concat([importacao_2020["geral_soma"], importacao_2021["geral_soma"]])
data["Geral - Exportação"] = pd.concat([exportacao_2020["geral_soma"], exportacao_2021["geral_soma"]])
data["Sólidos a Granel - Importação"] = pd.concat([importacao_2020["solidos_granel_soma"], importacao_2021["solidos_granel_soma"]])
data["Sólidos a Granel - Exportação"] = pd.concat([exportacao_2020["solidos_granel_soma"], exportacao_2021["solidos_granel_soma"]])
data = data.melt(ignore_index=False).reset_index()
data["mil_ton"] = data.value/1_000_000

plt.subplots(figsize=cg.FIGSIZE)
sns.set_context(rc = {'patch.linewidth': 0.0})
sns.barplot(data=data, x="index", y="mil_ton", hue="variable")


plt.xlabel ("Mês")
plt.ylabel ("Total Movimentado ($10^6$ ton)")
plt.legend ()

plt.tight_layout()
plt.savefig('porto_geral_granel' + cg.EXT)


# MEDIA EMISSAO VEICULAR
plt.subplots(figsize=cg.FIGSIZE_HALF)
sns.barplot(x=list(range(2015,2021)), y=
            [
                246241/(12*1000), 
                192873/(12*1000), 
                321827/(12*1000), 
                278239/(12*1000), 
                198637/(12*1000), 
                162753/(12*1000)
                ], color="C0")

if cg.ENGLISH:
    plt.xlabel ("Year")
    plt.ylabel ("Avg. Vehicles/month")
else:
    plt.xlabel ("Ano")
    plt.ylabel ("Média veículos/mês")
    

plt.tight_layout()
plt.savefig('porto_veiculos_automotores' + cg.EXT)
plt.show()


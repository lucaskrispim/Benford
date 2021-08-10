#!/usr/bin/python3
import pandas as pd
from frequency import freqabs, freqrel
from numpy import log10
import scipy.stats as stats

# boletimDeUrna = [
#     'data/2002/votacao_candidato_munzona_2002_BR.txt',
#     'data/2002/votacao_candidato_munzona_2002_ZZ.txt'
# ]
# colunas = {
#     'NR_TURNO' : 3,
#     'DS_CARGO_PERGUNTA' : 15,
#     'NM_MUNICIPIO' : 8,
#     'NM_VOTAVEL' : 14,
#     'QT_VOTOS' : 28
# }
# filtro = {
#     'NR_TURNO' : 2,
#     'DS_CARGO_PERGUNTA' : 'PRESIDENTE'
# }
# cabecalho = False

# boletimDeUrna = [
#     'data/2006/votacao_candidato_munzona_2006_BR.txt',
#     'data/2006/votacao_candidato_munzona_2006_ZZ.txt'
# ]
# colunas = {
#     'NR_TURNO' : 3,
#     'DS_CARGO_PERGUNTA' : 15,
#     'NM_MUNICIPIO' : 8,
#     'NM_VOTAVEL' : 14,
#     'QT_VOTOS' : 28
# }
# filtro = {
#     'NR_TURNO' : 2,
#     'DS_CARGO_PERGUNTA' : 'PRESIDENTE'
# }
# cabecalho = False

# boletimDeUrna = [
#     'data/2010/votacao_candidato_munzona_2010_BR.txt',
#     'data/2010/votacao_candidato_munzona_2010_VT.txt',
#     'data/2010/votacao_candidato_munzona_2010_ZZ.txt'
# ]
# colunas = {
#     'NR_TURNO' : 3,
#     'DS_CARGO_PERGUNTA' : 15,
#     'NM_MUNICIPIO' : 8,
#     'NM_VOTAVEL' : 14,
#     'QT_VOTOS' : 28
# }
# filtro = {
#     'NR_TURNO' : 2,
#     'DS_CARGO_PERGUNTA' : 'PRESIDENTE'
# }
# cabecalho = False

boletimDeUrna = [
    "data/2014/bweb_2t_AC_28102014114450.txt",
    "data/2014/bweb_2t_AL_28102014114941.txt",
    "data/2014/bweb_2t_AM_28102014115349.txt",
    "data/2014/bweb_2t_AP_28102014115835.txt",
    "data/2014/bweb_2t_BA_28102014120236.txt",
    "data/2014/bweb_2t_CE_28102014120643.txt",
    "data/2014/bweb_2t_DF_28102014121036.txt",
    "data/2014/bweb_2t_ES_28102014121431.txt",
    "data/2014/bweb_2t_GO_28102014121839.txt",
    "data/2014/bweb_2t_MA_28102014122307.txt",
    "data/2014/bweb_2t_MG_28102014122730.txt",
    "data/2014/bweb_2t_MS_28102014123155.txt",
    "data/2014/bweb_2t_MT_28102014123633.txt",
    "data/2014/bweb_2t_PA_28102014124021.txt",
    "data/2014/bweb_2t_PB_28102014124426.txt",
    "data/2014/bweb_2t_PE_28102014124827.txt",
    "data/2014/bweb_2t_PI_28102014125213.txt",
    "data/2014/bweb_2t_PR_28102014125604.txt",
    "data/2014/bweb_2t_RJ_28102014130047.txt",
    "data/2014/bweb_2t_RN_28102014130526.txt",
    "data/2014/bweb_2t_RO_28102014130948.txt",
    "data/2014/bweb_2t_RR_28102014131402.txt",
    "data/2014/bweb_2t_RS_28102014131811.txt",
    "data/2014/bweb_2t_SC_28102014132154.txt",
    "data/2014/bweb_2t_SE_28102014132556.txt",
    "data/2014/bweb_2t_SP_28102014133018.txt",
    "data/2014/bweb_2t_TO_28102014133436.txt",
    "data/2014/bweb_2t_ZZ_28102014133904.txt"
]
colunas = {
    'DS_CARGO_PERGUNTA' : 6,
    'NM_MUNICIPIO' : 13,
    'NM_VOTAVEL' : 22,
    'QT_VOTOS' : 23
}
filtro = {
    'DS_CARGO_PERGUNTA' : 'PRESIDENTE'
}
cabecalho = False
ttl = '2° TURNO DA ELEIÇÃO 2014'

# boletimDeUrna = [
#     "data/2018/bweb_2t_AC_301020181744.csv",
#     "data/2018/bweb_2t_AL_301020181745.csv",
#     "data/2018/bweb_2t_AM_301020181745.csv",
#     "data/2018/bweb_2t_AP_301020181746.csv",
#     "data/2018/bweb_2t_BA_301020181746.csv",
#     "data/2018/bweb_2t_CE_301020181747.csv",
#     "data/2018/bweb_2t_DF_301020181747.csv",
#     "data/2018/bweb_2t_ES_301020181748.csv",
#     "data/2018/bweb_2t_GO_301020181748.csv",
#     "data/2018/bweb_2t_MA_301020181749.csv",
#     "data/2018/bweb_2t_MG_301020181749.csv",
#     "data/2018/bweb_2t_MS_301020181750.csv",
#     "data/2018/bweb_2t_MT_301020181750.csv",
#     "data/2018/bweb_2t_PA_301020181751.csv",
#     "data/2018/bweb_2t_PB_301020181751.csv",
#     "data/2018/bweb_2t_PE_301020181752.csv",
#     "data/2018/bweb_2t_PI_301020181752.csv",
#     "data/2018/bweb_2t_PR_301020181753.csv",
#     "data/2018/bweb_2t_RJ_301020181753.csv",
#     "data/2018/bweb_2t_RN_301020181754.csv",
#     "data/2018/bweb_2t_RO_301020181754.csv",
#     "data/2018/bweb_2t_RR_301020181755.csv",
#     "data/2018/bweb_2t_RS_301020181755.csv",
#     "data/2018/bweb_2t_SC_301020181756.csv",
#     "data/2018/bweb_2t_SE_301020181756.csv",
#     "data/2018/bweb_2t_SP_301020181756.csv",
#     "data/2018/bweb_2t_TO_301020181757.csv",
#     "data/2018/bweb_2t_ZZ_301020181758.csv"
# ]
# colunas = {
#     'DS_CARGO_PERGUNTA' : 16,
#     'NM_MUNICIPIO' : 11,
#     'NM_VOTAVEL' : 28,
#     'QT_VOTOS' : 29
# }
# filtro = {
#     'DS_CARGO_PERGUNTA' : 'Presidente'
# }
# cabecalho = True

def Chi_Square(obs_freq, exp_freq):
    count = len(obs_freq)
    chi_sq = 0
    for i in range(count):
        x = (obs_freq[i] - exp_freq[i]) ** 2
        x = x / exp_freq[i]
        chi_sq += x
    return chi_sq

print("Lendo:", boletimDeUrna[0])
dfabs = freqabs(boletimDeUrna[0], colunas, filtro, cabecalho)
dfrel = freqrel(boletimDeUrna[0], colunas, filtro, cabecalho)
cols = dfabs.columns
for bu in boletimDeUrna[1:]:
    print("Lendo:", bu)
    dfAux = freqabs(bu, colunas, filtro, cabecalho)
    if(dfAux.size > 0):
        for col in cols:
            dfabs[col] = dfabs[col] + dfAux[col]

    dfAux = freqrel(bu, colunas, filtro, cabecalho)
    if(dfAux.size > 0):
        for col in cols:
            dfrel[col] = dfrel[col] + dfAux[col]

dfabs['DÍGITO'] = range(1, 10)

if(dfAux.size > 0):
    for col in cols:
        total = dfrel[col].sum()
        dfrel[col] = 100.0*dfrel[col]/total

dfrel['DÍGITO'] = range(1, 10)
for col in cols:
    total = dfabs[col].sum()
    dfabs['LEI DE BENFORD'] = [round(total*(log10(x + 1) - log10(x))) for x in range(1, 10)]
    chi2, p = stats.chisquare(f_obs = dfabs[col], f_exp = dfabs['LEI DE BENFORD'])
    print(f"{dfabs[[col, 'LEI DE BENFORD']]}")
    print(f"chi^2 = {chi2}, p = {p}")
    print("---")
    dfrel['LEI DE BENFORD'] = [100.0*(log10(x + 1) - log10(x)) for x in range(1, 10)]
    ax = dfrel.plot.line(x = 'DÍGITO', y = 'LEI DE BENFORD', ylabel = 'FREQUÊNCIA (%)', title = ttl, rot = 0, linestyle = '-', marker = 'o', color = '#00923e', use_index = False)
    dfrel.plot.bar(x = 'DÍGITO', y = col, ylabel = 'FREQUÊNCIA (%)', title = ttl, rot = 0, color = '#28166f', ax = ax)
    ax.figure.savefig(f"{col}.png")

print(dfabs)
print("---")
print(dfrel)
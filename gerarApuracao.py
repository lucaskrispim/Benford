#!/usr/bin/python3
from src.BoletimDeUrna import *

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
turno = 1
ano = 2018

# arquivos = [
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AC_14102014131600.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AL_14102014131724.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AM_14102014131956.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AP_14102014132239.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_BA_14102014132437.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_CE_14102014132811.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_DF_14102014133057.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_ES_14102014133258.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_GO_14102014133534.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MA_14102014133746.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MG_14102014133941.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MS_14102014134342.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MT_14102014134508.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PA_14102014134622.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PE_14102014134940.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PI_14102014135200.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PR_14102014135330.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RJ_14102014135555.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RN_14102014140015.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RO_14102014140131.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RR_14102014140241.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RS_14102014140344.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SC_14102014140606.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SE_14102014140814.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SP_14102014140937_parte1.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SP_14102014140937_parte2.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SP_14102014140937_parte3.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_TO_14102014141909.txt",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_ZZ_14102014142031.txt"
# ]

# # arquivos = [
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_AC_28102014114450.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_AL_28102014114941.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_AM_28102014115349.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_AP_28102014115835.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_BA_28102014120236.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_CE_28102014120643.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_DF_28102014121036.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_ES_28102014121431.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_GO_28102014121839.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_MA_28102014122307.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_MG_28102014122730.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_MS_28102014123155.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_MT_28102014123633.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_PA_28102014124021.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_PB_28102014124426.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_PE_28102014124827.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_PI_28102014125213.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_PR_28102014125604.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_RJ_28102014130047.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_RN_28102014130526.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_RO_28102014130948.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_RR_28102014131402.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_RS_28102014131811.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_SC_28102014132154.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_SE_28102014132556.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_SP_28102014133018.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_TO_28102014133436.txt",
# #     f"{dirbase}{ano}/bu/bweb_{turno}t_ZZ_28102014133904.txt",
# # ]

# colunas = {
#     "SG_UF" : 4,
#     "NM_MUNICIPIO" : 13,
#     "NR_ZONA" : 7,
#     "NR_SECAO" : 8,
#     "DS_CARGO_PERGUNTA" : 6,
#     "NM_VOTAVEL" : 22,
#     "QT_VOTOS" : 23
# }
# filtro = {
#     "DS_CARGO_PERGUNTA" : "PRESIDENTE"
# }
# cabecalho = False

arquivos = [
    f"{dirbase}{ano}/bu/bweb_{turno}t_AC_101020181938.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_AL_101020181938.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_AM_101020181939.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_AP_101020181940.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_BA_101020181941.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_CE_101020181945.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_DF_101020181947.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_ES_101020181949.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_GO_101020181950.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_MA_101020181952.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_MG_101020181954_parte1.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_MG_101020181954_parte2.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_MS_101020182001.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_MT_101020182002.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_PA_101020182003.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_PB_101020182005.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_PE_101020182006.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_PI_101020182009.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_PR_101020182010.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RJ_101020182014_parte1.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RJ_101020182014_parte2.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RN_101020182021.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RO_101020182022.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RR_101020182023.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_RS_101020182024.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SC_101020182028.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SE_101020182030.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SP_101020182030_parte1.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SP_101020182030_parte2.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SP_101020182030_parte3.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_SP_101020182030_parte4.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_TO_101020182047.csv",
    f"{dirbase}{ano}/bu/bweb_{turno}t_ZZ_111020181508.csv"
]
# arquivos = [
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AC_301020181744.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AL_301020181745.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AM_301020181745.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_AP_301020181746.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_BA_301020181746.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_CE_301020181747.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_DF_301020181747.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_ES_301020181748.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_GO_301020181748.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MA_301020181749.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MG_301020181749.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MS_301020181750.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_MT_301020181750.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PA_301020181751.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PB_301020181751.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PE_301020181752.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PI_301020181752.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_PR_301020181753.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RJ_301020181753.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RN_301020181754.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RO_301020181754.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RR_301020181755.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_RS_301020181755.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SC_301020181756.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SE_301020181756.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_SP_301020181756.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_TO_301020181757.csv",
#     f"{dirbase}{ano}/bu/bweb_{turno}t_ZZ_301020181758.csv"
# ]
colunas = {
    "SG_UF" : 9,
    "NM_MUNICIPIO" : 11,
    "NR_ZONA" : 12,
    "NR_SECAO" : 13,
    "DS_CARGO_PERGUNTA" : 16,
    "NM_VOTAVEL" : 28,
    "QT_VOTOS" : 29
}
filtro = {
    "DS_CARGO_PERGUNTA" : "Presidente"
}
cabecalho = True

agrupamentos = {
    "ESTADO": {
        "arquivo": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-estado.csv",
        "agrupamento": ["SG_UF", "NM_VOTAVEL"]
    },
    "MUNICÍPIO": {
        "arquivo": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-municipio.csv",
        "agrupamento": ["SG_UF", "NM_MUNICIPIO", "NM_VOTAVEL"]
    },
    "ZONA": {
        "arquivo": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-zona.csv",
        "agrupamento": ["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NM_VOTAVEL"]
    },
    "SEÇÃO": {
        "arquivo": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-secao.csv",
        "agrupamento": ["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NM_VOTAVEL"]
    }
}

boletimDeUrna = BoletimDeUrna()

for agr in agrupamentos:
    print(f"APURAÇÃO AGRUPADA POR {agr}")
    bu = boletimDeUrna.apurar(arquivos, colunas, filtro, agrupamentos[agr]["agrupamento"], cabecalho)
    boletimDeUrna.salvar(agrupamentos[agr]["arquivo"])
    print("")
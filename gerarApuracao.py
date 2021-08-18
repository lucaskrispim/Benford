#!/usr/bin/python3
from src.BoletimDeUrna import *
from csv import QUOTE_ALL

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
turno = 1
ano = 2018

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

boletimDeUrna = BoletimDeUrna()

print("Apuração agrupada por Estado")
agrupamento = ["SG_UF", "NM_VOTAVEL"]
bu = boletimDeUrna.apurar(arquivos, colunas, filtro, agrupamento, cabecalho)
boletimDeUrna.salvar(f"{dirbase}apuracao-{turno}t-{ano}-estado.csv")
print("")

print("Apuração agrupada por Município")
agrupamento = ["SG_UF", "NM_MUNICIPIO", "NM_VOTAVEL"]
bu = boletimDeUrna.apurar(arquivos, colunas, filtro, agrupamento, cabecalho)
boletimDeUrna.salvar(f"{dirbase}apuracao-{turno}t-{ano}-municipio.csv")
print("")

print("Apuração agrupada por Zona")
agrupamento = ["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NM_VOTAVEL"]
bu = boletimDeUrna.apurar(arquivos, colunas, filtro, agrupamento, cabecalho)
boletimDeUrna.salvar(f"{dirbase}apuracao-{turno}t-{ano}-zona.csv")
print("")

print("Apuração agrupada por Seção")
agrupamento = ["SG_UF", "NM_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NM_VOTAVEL"]
bu = boletimDeUrna.apurar(arquivos, colunas, filtro, agrupamento, cabecalho)
boletimDeUrna.salvar(f"{dirbase}apuracao-{turno}t-{ano}-secao.csv")
#!/usr/bin/python3
from src.BoletimDeUrna import *
from csv import QUOTE_ALL

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
cabecalho = True
turno = 1
ano = 2018

print(f"FREQUÊNCIA ABSOLUTA AGRUPADA POR ESTADO")
boletimDeUrna = BoletimDeUrna(f"{dirbase}{ano}/apuracao-{turno}t-{ano}-estado.csv", cabecalho)
total = len(boletimDeUrna._boletimDeUrna["SG_UF"].unique())
frequenciaEsperada = [total*boletimDeUrna._leiDeBenford[i] for i in range(9)]
frequenciaAbsoluta = boletimDeUrna.frequenciaAbsoluta()
for nome in frequenciaAbsoluta.columns:
    print(f"{nome}  ", end = "")
    for fq in frequenciaAbsoluta[nome]:
        print(f"{fq:5.2f}  ", end = "")

    print("")

print("")

for nome in frequenciaAbsoluta.columns:
    erroRelativo = boletimDeUrna.erroRelativo(frequenciaAbsoluta[nome], frequenciaEsperada)
    print(f"{nome}  ", end = "")
    for err in erroRelativo:
        print(f"{err:5.2f}  ", end = "")

    print("")

print("")

orderDeGrandeza = boletimDeUrna.ordemDeGrandeza()
for odg in orderDeGrandeza:
    print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")

print("")

print(f"FREQUÊNCIA ABSOLUTA AGRUPADA POR MUNICÍPIO")
boletimDeUrna = BoletimDeUrna(f"{dirbase}{ano}/apuracao-{turno}t-{ano}-municipio.csv", cabecalho)
total = 0
estados = boletimDeUrna._boletimDeUrna["SG_UF"].unique()
for estado in estados:
    est = boletimDeUrna._boletimDeUrna.loc[boletimDeUrna._boletimDeUrna["SG_UF"] == estado]
    total += len(est["NM_MUNICIPIO"].unique())

frequenciaEsperada = [total*boletimDeUrna._leiDeBenford[i] for i in range(9)]
frequenciaAbsoluta = boletimDeUrna.frequenciaAbsoluta()
for nome in frequenciaAbsoluta.columns:
    print(f"{nome}  ", end = "")
    for fq in frequenciaAbsoluta[nome]:
        print(f"{fq}  ", end = "")

    print("")

print("")

for nome in frequenciaAbsoluta.columns:
    erroRelativo = boletimDeUrna.erroRelativo(frequenciaAbsoluta[nome], frequenciaEsperada)
    print(f"{nome}  ", end = "")
    for err in erroRelativo:
        print(f"{err:5.2f}  ", end = "")

    print("")

print("")

orderDeGrandeza = boletimDeUrna.ordemDeGrandeza()
for odg in orderDeGrandeza:
    print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")

print("")

print(f"FREQUÊNCIA ABSOLUTA AGRUPADA POR ZONA")
boletimDeUrna = BoletimDeUrna(f"{dirbase}{ano}/apuracao-{turno}t-{ano}-zona.csv", cabecalho)
total = 0
estados = boletimDeUrna._boletimDeUrna["SG_UF"].unique()
for estado in estados:
    est = boletimDeUrna._boletimDeUrna.loc[boletimDeUrna._boletimDeUrna["SG_UF"] == estado]
    municipios = est["NM_MUNICIPIO"].unique()
    for municipio in municipios:
        zona = est.loc[est["NM_MUNICIPIO"] == municipio]
        total += len(zona["NR_ZONA"].unique())

frequenciaEsperada = [total*boletimDeUrna._leiDeBenford[i] for i in range(9)]
frequenciaAbsoluta = boletimDeUrna.frequenciaAbsoluta()
for nome in frequenciaAbsoluta.columns:
    print(f"{nome}  ", end = "")
    for fq in frequenciaAbsoluta[nome]:
        print(f"{fq}  ", end = "")

    print("")

print("")

for nome in frequenciaAbsoluta.columns:
    erroRelativo = boletimDeUrna.erroRelativo(frequenciaAbsoluta[nome], frequenciaEsperada)
    print(f"{nome}  ", end = "")
    for err in erroRelativo:
        print(f"{err:5.2f}  ", end = "")

    print("")

print("")

orderDeGrandeza = boletimDeUrna.ordemDeGrandeza()
for odg in orderDeGrandeza:
    print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")

print("")

print(f"FREQUÊNCIA ABSOLUTA AGRUPADA POR SEÇÃO")
boletimDeUrna = BoletimDeUrna(f"{dirbase}{ano}/apuracao-{turno}t-{ano}-secao.csv", cabecalho)
total = 0
estados = boletimDeUrna._boletimDeUrna["SG_UF"].unique()
for estado in estados:
    est = boletimDeUrna._boletimDeUrna.loc[boletimDeUrna._boletimDeUrna["SG_UF"] == estado]
    municipios = est["NM_MUNICIPIO"].unique()
    for municipio in municipios:
        mun = est.loc[est["NM_MUNICIPIO"] == municipio]
        zonas = mun["NR_ZONA"].unique()
        for zona in zonas:
            zon = mun.loc[mun["NR_ZONA"] == zona]
            secoes = zon["NR_SECAO"].unique()
            total += len(secoes)

frequenciaEsperada = [total*boletimDeUrna._leiDeBenford[i] for i in range(9)]
frequenciaAbsoluta = boletimDeUrna.frequenciaAbsoluta()
for nome in frequenciaAbsoluta.columns:
    print(f"{nome}  ", end = "")
    for fq in frequenciaAbsoluta[nome]:
        print(f"{fq}  ", end = "")

    print("")

print("")

for nome in frequenciaAbsoluta.columns:
    erroRelativo = boletimDeUrna.erroRelativo(frequenciaAbsoluta[nome], frequenciaEsperada)
    print(f"{nome}  ", end = "")
    for err in erroRelativo:
        print(f"{err:5.2f}  ", end = "")

    print("")

print("")

orderDeGrandeza = boletimDeUrna.ordemDeGrandeza()
for odg in orderDeGrandeza:
    print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")

print("")
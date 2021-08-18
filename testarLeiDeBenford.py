#!/usr/bin/python3
from src.BoletimDeUrna import *
from csv import QUOTE_ALL

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
cabecalho = True
turno = 1
ano = 2018

agrupamento = {
    "Estado" : f"{dirbase}{ano}/apuracao-{turno}t-{ano}-estado.csv",
    "Município": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-municipio.csv",
    "Zona": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-zona.csv",
    "Seção": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-secao.csv",
}

for agr in agrupamento:
    print(f"Frequência relativa agrupada por {agr}")
    boletimDeUrna = BoletimDeUrna(agrupamento[agr], cabecalho)
    frequenciaRelativa = boletimDeUrna.frequenciaRelativa()
    for nome in frequenciaRelativa.columns:
        print(f"{nome}  ", end = "")
        for fq in frequenciaRelativa[nome]:
            print(f"{fq:5.2f}  ", end = "")

        print("")

    print("")

    orderDeGrandeza = boletimDeUrna.orderDeGrandeza()
    for odg in orderDeGrandeza:
        print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")
    
    print("")

    testeDeAderencia = boletimDeUrna.testeDeAderencia()
    print(f"chi2Critico = {testeDeAderencia['chi2Critico']:5.2f}, alfa = {testeDeAderencia['alfa']:5.2f}, grauDeLiberdade = {testeDeAderencia['grauDeLiberdade']}")
    for nome in testeDeAderencia["NM_VOTAVEL"]:
        print(f"{nome}  {testeDeAderencia['NM_VOTAVEL'][nome]['teste']}  {testeDeAderencia['NM_VOTAVEL'][nome]['chi2']:5.2f}  {testeDeAderencia['NM_VOTAVEL'][nome]['p']:5.2f}")
    
    print("")
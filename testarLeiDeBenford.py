#!/usr/bin/python3
from src.BoletimDeUrna import *
from csv import QUOTE_ALL

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
cabecalho = True
turno = 1
ano = 2018

agrupamentos = {
    "ESTADO": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-estado.csv",
    "MUNICÍPIO": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-municipio.csv",
    "ZONA": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-zona.csv",
    "SEÇÃO": f"{dirbase}{ano}/apuracao-{turno}t-{ano}-secao.csv"
}

for agrupamento in agrupamentos:
    titulo = f"FREQUÊNCIA ABSOLUTA AGRUPADA POR {agrupamento}"
    print(titulo)
    boletimDeUrna = BoletimDeUrna(agrupamentos[agrupamento], cabecalho)
    frequenciaAbsoluta = boletimDeUrna.frequenciaAbsoluta()
    for nome in frequenciaAbsoluta.columns:
        print(f"{nome}  ", end = "")
        for fq in frequenciaAbsoluta[nome]:
            print(f"{fq:5.2f}  ", end = "")

        print("")

    print("")

    for nome in frequenciaAbsoluta.columns:
        total = frequenciaAbsoluta[nome].sum()
        frequenciaEsperada = [total*boletimDeUrna._leiDeBenford[i] for i in range(9)]
        erroRelativo = boletimDeUrna.erroRelativo(frequenciaAbsoluta[nome], frequenciaEsperada)
        print(f"{nome}  ", end = "")
        for err in erroRelativo:
            print(f"{err:5.2f}  ", end = "")

        boletimDeUrna.grafico(nome, f"{dirbase}frequencia-absoluta-{nome}-{turno}t-{ano}-{agrupamento}.png", titulo + f" - {nome}")
        print("")

    print("")

    orderDeGrandeza = boletimDeUrna.ordemDeGrandeza()
    for odg in orderDeGrandeza:
        print(f"{odg}  {orderDeGrandeza[odg]['minimo']}  {orderDeGrandeza[odg]['maximo']}  10^{orderDeGrandeza[odg]['ordem']}")

    print("")
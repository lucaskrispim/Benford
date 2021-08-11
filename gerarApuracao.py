#!/usr/bin/python3
from os import path
from BoletimDeUrna import apurar, freqabs
from csv import QUOTE_ALL
"""
    O TSE disponibiliza no endereço [1] os arquivos do boletim de urna (BU)
    separados por cada estado brasileiro. O arquivo do BU contém os dados
    brutos que saem da urna eletrônica e possuem diversas informações como,
    por exemplo, o número do turno, a descrição do cargo/pergunta, o nome do município,
    o nome do votável e a quantidade de votos.

    Neste exemplo, considere que dentro do diretório "eleicoes/" estão os arquivos
    "bweb_1t_AA_010120180000.csv", "bweb_1t_AB_010120180000.csv" e
    "bweb_1t_AC_010120180000.csv". Esses arquivos serão processados para extrair
    as colunas indicadas na variável "colunas", de tal forma que a coluna
    "DS_CARGO_PERGUNTA" deverá ser igual a "Presidente".

    Após o processamento, serão criados os arquivos "apuracao-t1-2018-AA.csv",
    "apuracao-t1-2018-AB.csv", "apuracao-t1-2018-AC.csv", 
    "frequencia-absoluta-t1-2018.csv" e "frequencia-relativa-t1-2018.csv".

    Referência
    [1] https://www.tse.jus.br/hotsites/pesquisas-eleitorais/resultados.html
"""

codificacao = "ISO-8859-1"
dirbase = "eleicoes/"
turno = 1
ano = 2018
boletimDeUrna = [
    'bweb_1t_AA_010120180000.csv',
    'bweb_1t_AB_010120180000.csv',
    'bweb_1t_AC_010120180000.csv',
]
colunas = {
    'DS_CARGO_PERGUNTA' : 16,
    'NM_MUNICIPIO' : 11,
    'NM_VOTAVEL' : 28,
    'QT_VOTOS' : 29
}
filtro = {
    'DS_CARGO_PERGUNTA' : 'Presidente'
}
cabecalho = True

totalDeArquivos = len(boletimDeUrna)
i = 0
dfabs = None
primeiroArquivo = True
while(i < totalDeArquivos):
    bu = dirbase + boletimDeUrna[i]
    print(f"Apurando: {bu}")
    df = apurar(bu, colunas, filtro, cabecalho)
    print(f"Total de registros apurados: {len(df)}") if df and len(df) > 0 else print(f"Size df is equal 0")
    if df and len(df) > 0:
        if(primeiroArquivo):
            dfabs = freqabs(df)
            primeiroArquivo = False
        else:
            dfAbsAux = freqabs(df)
            dfabs += dfAbsAux

        buArquivo = path.basename(boletimDeUrna[i])
        estado = buArquivo[8:10]
        if(buArquivo.find("parte") < 0):
            parte = ""
        else:
            parte = "-" + buArquivo[buArquivo.find("parte"):buArquivo.find(".")]

        print(f"Salvando arquivo: {dirbase}apuracao-t{turno}-{ano}-{estado}{parte}.csv")
        df.to_csv(f"{dirbase}apuracao-t{turno}-{ano}-{estado}{parte}.csv", sep = ";", header = True, index = False, quoting = QUOTE_ALL, encoding = codificacao)
    i += 1

if dfabs and dfabs.columns:
    cols = dfabs.columns
    dfrel = dfabs.copy()
    for col in cols:
        total = dfrel[col].sum()
        dfrel[col] = 100.0*dfrel[col]/total

    dfabs["DÍGITO"] = range(1, 10)
    dfrel["DÍGITO"] = range(1, 10)
    print(f"{dirbase}frequencia-absoluta-t{turno}-{ano}.csv")
    dfabs.to_csv(f"{dirbase}frequencia-absoluta-t{turno}-{ano}.csv", sep = ";", header = True, index = False, quoting = QUOTE_ALL, encoding = codificacao)
    print(f"{dirbase}frequencia-relativa-t{turno}-{ano}.csv")
    dfrel.to_csv(f"{dirbase}frequencia-relativa-t{turno}-{ano}.csv", sep = ";", header = True, index = False, quoting = QUOTE_ALL, encoding = codificacao)
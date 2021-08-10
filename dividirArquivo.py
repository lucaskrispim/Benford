#!/usr/bin/python3
from BoletimDeUrna import dividirArquivo

"""
    O arquivo de boletim de urna pode conter uma quantidade muito grande de
    linhas para que seja processado por alguns computadores com pouca memória
    disponível.

    Neste exemplo, o arquivo "exemplo.csv" será dividido nos arquivos
    "exemplo_parte1.csv", "exemplo_parte2.csv", …, "exemplo_parten.csv",
    onde cada arquivo criado terá (no máximo) 5 milhões de linhas.
"""
nomeDoArquivo = "exemplo.csv"
quantidadeDeLinhas = 5000000
prefixoDaSaida = "exemplo_parte"
dividirArquivo(nomeDoArquivo, quantidadeDeLinhas, prefixoDaSaida)

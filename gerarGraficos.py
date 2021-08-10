#!/usr/bin/python3
import pandas as pd
from BoletimDeUrna import gerarGrafico
"""
    Neste exemplo, considere que dentro do diretório "eleicoes/2018" está o arquivo
    "frequencia-relativa-t1-2018.csv" que foi gerado pelo script
    "gerarApuracao.py".

    O arquivo será processado para gerar o gráfico de linha da lei de Benford
    juntamente com a frequência relativa obtida de cada candidato. No final do
    processamento serão criados os arquivos de imagem "frequencia-relativa-t1-2018.png",
    "candidato1-frequencia-relativa-t1-2018.png", "candidato2-frequencia-relativa-t1-2018.png", …,
    "candidaton-frequencia-relativa-t1-2018.png".
"""

turno = 1
ano = 2018
arquivoFrequenciaRelativa = f"eleicoes/{ano}/frequencia-relativa-t{turno}-{ano}.csv"
arquivoGrafico = f"eleicoes/{ano}/frequencia-relativa-t{turno}-{ano}.png"
codificacao = "ISO-8859-1"
delimitador = ";"
titulo = f"{turno}° TURNO DA ELEIÇÃO {ano}"

frel = pd.read_csv(arquivoFrequenciaRelativa, encoding = codificacao, delimiter = delimitador)
nomeDoVotavel = list(frel.columns)
nomeDoVotavel = [nome.upper() for nome in nomeDoVotavel]
retirar = ["BRANCO", "NULO", "DÍGITO"]
for r in retirar:
    nomeDoVotavel.remove(r)

nomeDoVotavel.append("BRANCO")
nomeDoVotavel.append("NULO")
gerarGrafico(frel, nomeDoVotavel, arquivoGrafico, titulo)
for nome in nomeDoVotavel:
    nm = nome.lower()
    nm = nm.replace(" ", "-")
    arquivoGrafico = f"eleicoes/{ano}/{nm}-frequencia-relativa-t{turno}-{ano}.png"
    gerarGrafico(frel, [nome], arquivoGrafico, titulo)
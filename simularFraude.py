#!/usr/bin/python3
import csv
import pandas as pd
from BoletimDeUrna import freqabs
"""
    @todo: [Colocar documentação]
"""
dirbase = "eleicoes/"
simulacao = "/simulacao/"
codificacao = "ISO-8859-1"
delimitador = ";"
estado = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT",
    "PA", "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP",
    "TO", "ZZ"
]
turno = '1'
ano = '2018'
quantidadeDeVotaveisNoPleito = 15
removerVoto = ["FERNANDO HADDAD", "BRANCO", "NULO"]
adicionarVoto = "JAIR BOLSONARO"
votaveisAlterados = {
    "FERNANDO HADDAD": {"ANTES" : 0, "DEPOIS" : 0},
    "JAIR BOLSONARO": {"ANTES" : 0, "DEPOIS" : 0},
    "BRANCO": {"ANTES" : 0, "DEPOIS" : 0},
    "NULO": {"ANTES" : 0, "DEPOIS" : 0}
}
ordemAlfabeticaDoVotavel = 9
porcentagem = 0.30
quantidadeDeVotos = 12100000
NM_MUNICIPIO = 0
NM_VOTAVEL = 1
QT_VOTOS = 2
for es in estado:
    print(f"Alterando votacao em: {es}...")
    arquivoApuracaoReal = f"{dirbase}{ano}/apuracao-t{turno}-{ano}-{es}.csv"
    arquivoApuracaoSimulada = f"{dirbase}{ano}{simulacao}/apuracao-t{turno}-{ano}-{es}.csv"
    apuracaoReal = open(arquivoApuracaoReal, encoding = codificacao)
    apuracaoSimulada = open(arquivoApuracaoSimulada, "w", encoding = codificacao)
    dfApuracaoReal = csv.reader(apuracaoReal, delimiter = delimitador)
    dfApuracaoSimulada = csv.writer(apuracaoSimulada, delimiter = delimitador, quoting=csv.QUOTE_ALL)
    indices = []
    totalDeIndices = 0
    novoArquivo = []
    indices = []
    for linha in dfApuracaoReal:
        if(linha[NM_VOTAVEL] == adicionarVoto):
            indices.append(totalDeIndices)
        novoArquivo.append(linha)
        totalDeIndices += 1

    for id in indices:
        if(quantidadeDeVotos > 0):
            if(id > ordemAlfabeticaDoVotavel):
                inicio = id - ordemAlfabeticaDoVotavel
            else:
                inicio = 0

            if(id + (quantidadeDeVotaveisNoPleito - ordemAlfabeticaDoVotavel - 1) < totalDeIndices):
                fim = id + (quantidadeDeVotaveisNoPleito - ordemAlfabeticaDoVotavel - 1)
            else:
                fim = totalDeIndices - 1

            totalDeVotos = 0
            removerVotoId = []
            for i in range(inicio, fim + 1):
                if((novoArquivo[i][NM_MUNICIPIO] == novoArquivo[id][NM_MUNICIPIO])):
                    totalDeVotos += int(novoArquivo[i][QT_VOTOS])
                    if(novoArquivo[i][NM_VOTAVEL] in removerVoto):
                        removerVotoId.append(i)

            vt = int(novoArquivo[id][QT_VOTOS])
            universoDeVotosParaRemover = totalDeVotos - vt
            quantidadeDeVotosParaRedistribuir = round(porcentagem*universoDeVotosParaRemover)
            retirados = 0
            if(quantidadeDeVotosParaRedistribuir > 0):
                retirar = {}
                for i in removerVotoId:
                    vt = int(novoArquivo[i][QT_VOTOS])
                    r = round(vt*quantidadeDeVotosParaRedistribuir/universoDeVotosParaRemover)
                    retirar[i] = r
                    retirados += r

                if(retirados > 0):
                    for i in removerVotoId:
                        if(quantidadeDeVotos - retirar[i] <= 0):
                            retirar[i] = quantidadeDeVotos

                        novoArquivo[i][QT_VOTOS] = str(int(novoArquivo[i][QT_VOTOS]) - retirar[i])
                        novoArquivo[id][QT_VOTOS] = str(int(novoArquivo[id][QT_VOTOS]) + retirar[i])
                        quantidadeDeVotos -= retirar[i]
                        if(quantidadeDeVotos <= 0):
                            break

                if(quantidadeDeVotos <= 0):
                    break

            if((quantidadeDeVotosParaRedistribuir == 0) or (retirados == 0)):
                print(f"{novoArquivo[id][NM_MUNICIPIO]}: nenhum voto retirado.")

    #Salvar arquivo
    for linha in novoArquivo:
        dfApuracaoSimulada.writerow(linha)

dfabs = None
primeiroArquivo = True
for es in estado:
    arquivoApuracaoReal = f"{dirbase}{ano}/apuracao-t{turno}-{ano}-{es}.csv"
    arquivoApuracaoSimulada = f"{dirbase}{ano}/simulacao/apuracao-t{turno}-{ano}-{es}.csv"
    dfApuracaoReal = pd.read_csv(arquivoApuracaoReal, encoding = codificacao, delimiter=';')
    dfApuracaoSimulada = pd.read_csv(arquivoApuracaoSimulada, encoding = codificacao, delimiter=';')

    if(primeiroArquivo):
        dfabs = freqabs(dfApuracaoSimulada)
        primeiroArquivo = False
    else:
        dfAbsAux = freqabs(dfApuracaoSimulada)
        dfabs += dfAbsAux
    
    for votavel in votaveisAlterados.keys():
        temp = dfApuracaoReal.loc[dfApuracaoReal["NM_VOTAVEL"] == votavel]
        votaveisAlterados[votavel]["ANTES"] += temp["QT_VOTOS"].sum()
        temp = dfApuracaoSimulada.loc[dfApuracaoSimulada["NM_VOTAVEL"] == votavel]
        votaveisAlterados[votavel]["DEPOIS"] += temp["QT_VOTOS"].sum()

cols = dfabs.columns
dfrel = dfabs.copy()
for col in cols:
    totalDeVotos = dfrel[col].sum()
    dfrel[col] = 100.0*dfrel[col]/totalDeVotos

dfabs["DÍGITO"] = range(1, 10)
dfrel["DÍGITO"] = range(1, 10)
print(f"Salvando arquivo: {dirbase}{ano}/simulacao/frequencia-absoluta-t{turno}-{ano}.csv")
dfabs.to_csv(f"{dirbase}{ano}/simulacao/frequencia-absoluta-t{turno}-{ano}.csv", sep = ";", header = True, index = False, quoting = csv.QUOTE_ALL, encoding = codificacao)
print(f"Salvando arquivo: {dirbase}{ano}/simulacao/frequencia-relativa-t{turno}-{ano}.csv")
dfrel.to_csv(f"{dirbase}{ano}/simulacao/frequencia-relativa-t{turno}-{ano}.csv", sep = ";", header = True, index = False, quoting = csv.QUOTE_ALL, encoding = codificacao)
print("\nALTERACOES")
for votavel in votaveisAlterados.keys():
    diferenca = votaveisAlterados[votavel]['DEPOIS'] - votaveisAlterados[votavel]['ANTES']
    print(f"{votavel}: {votaveisAlterados[votavel]['ANTES']}  {votaveisAlterados[votavel]['DEPOIS']}  {diferenca}  (FATOR: {(diferenca/votaveisAlterados[votavel]['ANTES']):5.2f})")
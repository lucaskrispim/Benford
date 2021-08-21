#!/usr/bin/python3
from src.BoletimDeUrna import *

dirbase = "/opt/eleicoes/"
codificacao = "ISO-8859-1"
cabecalho = True
turno = 1
ano = 2018

removerVoto = ["FERNANDO HADDAD", "BRANCO", "NULO"]
adicionarVoto = "JAIR BOLSONARO"
votaveis = removerVoto.copy()
votaveis.append(adicionarVoto)
quantidadeDeVotos = 12000000
porcentagem = 0.9
quantidadeDeVotaveisNoPleito = 15
ordemAlfabeticaDoVotavelParaAdicionar = 9
local = {
    "SP" : [],
    "MG" : [],
    "RJ" : [],
    "ES" : []
}

agrupamentoMunicipio = f"{dirbase}{ano}/apuracao-{turno}t-{ano}-municipio.csv"
novoAgrupamentoMunicipio = f"{dirbase}{ano}/simulacao/apuracao-{turno}t-{ano}-municipio.csv"

boletimDeUrna = BoletimDeUrna(agrupamentoMunicipio, cabecalho)
apuracao = {}
for votavel in votaveis:
    votos = boletimDeUrna._boletimDeUrna.loc[(boletimDeUrna._boletimDeUrna["SG_UF"].isin(local.keys())) & (boletimDeUrna._boletimDeUrna["NM_VOTAVEL"] == votavel)]
    apuracao[votavel] = {
        "ANTES" : votos['QT_VOTOS'].sum(),
        "DEPOIS" : 0
    }

print("")

boletimDeUrna.transferirVoto(agrupamentoMunicipio, novoAgrupamentoMunicipio, removerVoto, adicionarVoto, porcentagem, quantidadeDeVotos, quantidadeDeVotaveisNoPleito, ordemAlfabeticaDoVotavelParaAdicionar, local)
for votavel in votaveis:
    votos = boletimDeUrna._boletimDeUrna.loc[(boletimDeUrna._boletimDeUrna["SG_UF"].isin(local.keys())) & (boletimDeUrna._boletimDeUrna["NM_VOTAVEL"] == votavel)]
    apuracao[votavel]["DEPOIS"] = votos['QT_VOTOS'].sum()
    print(f"{votavel}    {apuracao[votavel]['ANTES']}    {apuracao[votavel]['DEPOIS']}    {apuracao[votavel]['DEPOIS'] - apuracao[votavel]['ANTES']}")

